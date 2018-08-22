import aiohttp
import time
from fake_useragent import UserAgent
from logzero import logger


class Proxy(dict):
    def __init__(self, host, port):
        super(Proxy, self).__init__(host=host, port=port)
        self.host = host
        self.port = port

    @property
    def proxy_url(self):
        return 'http://{}:{}'.format(self.host, self.port)

    async def test_url(self, url):
        async with aiohttp.ClientSession() as session:
            header = {
                'User-Agent': UserAgent().random
            }
            try:
                start = time.time()
                async with session.get(url, headers=header, proxy=self.proxy_url, timeout=20, ssl=False) as res:
                    await res.text()
                    elpased = time.time() - start
                    logger.info("proxy {} elpased {}".format(
                        self.proxy_url, elpased))
                    return (elpased, self.proxy_url)

            except Exception:
                return (float('inf'), self.proxy_url)

    async def test_google(self):
        return await self.test_url('https://www.google.com')

    async def test_baidu(self):
        return await self.test_url('https://www.baidu.com')

    async def test_httpbin(self):
        return await self.test_url('http://www.httpbin.org')
