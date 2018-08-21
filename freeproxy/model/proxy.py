from config import TEST_URL
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

    async def test(self):
        async with aiohttp.ClientSession() as session:
            header = {
                'User-Agent': UserAgent().random
            }
            try:
                start = time.time()
                async with session.get(TEST_URL, headers=header, proxy=self.proxy_url, timeout=20, ssl=False) as res:
                    await res.text()
                    elpased = time.time() - start
                    logger.info("proxy {} elpased {}".format(
                        self.proxy_url, elpased))
                    return (elpased, self.proxy_url)

            except Exception:
                return (float('inf'), self.proxy_url)
