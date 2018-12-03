import time

import aiohttp
from dummy_useragent import UserAgent
from logzero import logger


class TestRst(dict):
    def __init__(self, elapsed, proxy):
        super(TestRst, self).__init__(proxy=proxy)
        self.elapsed = elapsed
        self.proxy = proxy

    def __lt__(self, other):
        return self.elapsed <= other.elapsed

    def __gt__(self, other):
        return self.elapsed > other.elapsed


class Proxy(dict):
    def __init__(self, host, port):
        super(Proxy, self).__init__(host=host, port=port)
        self.host = host
        self.port = port

    @property
    def proxy(self):
        return '{}:{}'.format(self.host, self.port)

    @property
    def proxy_url(self):
        return 'http://{}:{}'.format(self.host, self.port)

    async def test_url(self, url):
        async with aiohttp.ClientSession() as session:
            header = {'User-Agent': UserAgent().random()}
            try:
                start = time.time()
                async with session.get(
                        url,
                        headers=header,
                        proxy=self.proxy_url,
                        timeout=30,
                        ssl=False) as res:
                    await res.text()
                    elpased = time.time() - start
                    logger.info("proxy {} elpased {}".format(
                        self.proxy, elpased))
                    return TestRst(elpased, self.proxy)

            except Exception:
                return TestRst(float('inf'), self.proxy)

    async def test_google(self):
        return await self.test_url('https://www.google.com')

    async def test_baidu(self):
        return await self.test_url('https://www.baidu.com')

    async def test_httpbin(self):
        return await self.test_url('http://www.httpbin.org')
