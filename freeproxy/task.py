import asyncio
import itertools
from freeproxy.channels import CHANS, Channel
from freeproxy.config import REFRESH_DELAY
from freeproxy.util.tools import Proxy
from freeproxy.util.log import logger
from freeproxy.util.db import getRedis


class Task(object):
    def __init__(self):
        logger.info("proxy pool task stared")
        self.client = getRedis()
        self.loop = asyncio.get_event_loop()

    async def grab(self, channel):
        assert issubclass(channel, Channel), "Not support Class"
        coro = channel().run()
        proxy_list = await asyncio.gather(coro)
        unique = set(list(itertools.chain(*itertools.chain(*proxy_list))))
        return unique

    async def test_http(self, proxies):
        tasks = []
        for inner in proxies:
            if not inner[0]:
                continue
            tasks.append(Proxy(*inner).test_baidu())
        rst = await asyncio.gather(*tasks)
        rst = list(filter(lambda x: x.elapsed != float('inf'), rst))
        rst = list(map(lambda x: x.proxy, rst))
        await self.client.sadd('https_proxy', *rst)

    async def test_https(self, proxies):
        tasks = []
        for inner in proxies:
            if not inner[0]:
                continue
            tasks.append(Proxy(*inner).test_httpbin())
        rst = await asyncio.gather(*tasks)
        rst = list(filter(lambda x: x.elapsed != float('inf'), rst))
        rst = list(map(lambda x: x.proxy, rst))
        await self.client.sadd('http_proxy', *rst)

    async def run(self):
        logger.info("grab stages start")
        grabs = [asyncio.ensure_future(self.grab(channel)) for channel in CHANS]
        rst = await asyncio.gather(*grabs)
        logger.info("grab stages end")
        logger.info("http test stage start")
        await self.test_http(rst)
        logger.info("http test stage end")
        logger.info("https test stage start")
        await self.test_https(rst)
        logger.info("https test stage end")
        logger.info("store stage start")

def main():
    loop = asyncio.get_event_loop()
    coro = Task().run()
    loop.run_until_complete(asyncio.ensure_future(coro))


if __name__ == '__main__':
    main()
