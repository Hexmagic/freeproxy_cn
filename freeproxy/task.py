import asyncio
import itertools
from concurrent.futures import ThreadPoolExecutor

from freeproxy.channels import CHANS, Channel
from freeproxy.config import PROXY_KEY, REFRESH_DELAY, SITE_NUM
from freeproxy.util.proxy import Proxy
from freeproxy.util.tools import getRedis

EXECUTOR = ThreadPoolExecutor(max_workers=SITE_NUM)


async def grab_and_store(channel):
    assert issubclass(channel, Channel), "Not support Class"
    client = getRedis()
    coro = channel().batch()
    proxy_list = await asyncio.gather(coro)
    unique = set(list(itertools.chain(*itertools.chain(*proxy_list))))
    tasks = []
    for inner in unique:
        if not inner[0]:
            continue
        tasks.append(Proxy(*inner).test_baidu())
    rst = await asyncio.gather(*tasks)
    rst = list(filter(lambda x: x.elapsed != float('inf'), rst))
    rst = list(map(lambda x: x.proxy, rst))
    if not rst:
        return
    await client.sadd(PROXY_KEY, *rst)
    print("channel {} test passed ".format(channel))


def startup():
    def func(channel):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        rst = new_loop.run_until_complete(
            asyncio.ensure_future(grab_and_store(channel)))
        return rst
    loop = asyncio.get_event_loop()
    [loop.run_in_executor(EXECUTOR, func, channel) for channel in CHANS]
    loop.call_later(REFRESH_DELAY, startup)


def main():
    loop = asyncio.get_event_loop()
    loop.call_soon(startup)
    loop.run_forever()


if __name__ == '__main__':
    main()
