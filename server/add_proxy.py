import asyncio
from freeproxy.channels import CHANS
import aredis
from config import PROXY_KEY, REDIS_DB, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT
from freeproxy.model import Proxy
import itertools
from concurrent.futures import ThreadPoolExecutor

from freeproxy.channels import CHANS, Channel


async def grab_and_store(channel):
    assert issubclass(channel, Channel), "Not support Class"
    client = aredis.StrictRedis(
        host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)
    coro = channel().batch()
    proxy_list = await asyncio.gather(coro)
    unique = set(list(itertools.chain(*itertools.chain(*proxy_list))))
    tasks = []
    for inner in unique:
        if not inner[0]:
            continue
        if str(inner[1]) == '80':
            continue
        tasks.append(Proxy(*inner).test())
    rst = await asyncio.gather(*tasks)
    rst = list(filter(lambda x: x[0] != float('inf'), rst))
    await client.sadd("proxy", *rst)
    print("channel {} test passed ".format(channel))


async def startup():
    def func(channel):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        rst = new_loop.run_until_complete(
            asyncio.ensure_future(grab_and_store(channel)))
        return rst
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(max_workers=7)
    [loop.run_in_executor(executor, func, channel) for channel in CHANS]


def main():
    coro = startup()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.ensure_future(coro))


if __name__ == '__main__':
    main()
