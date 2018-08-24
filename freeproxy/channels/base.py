from collections import defaultdict
import aiohttp
import asyncio
from freeproxy.util.log import logger
from freeproxy.config import DEBUG_FLAG, DEBUG_PORXY
from freeproxy.util.pipe import to_doc, extra_xpath, safe_extra
from fake_useragent import UserAgent
import traceback

__all__ = ('Channel')


class Channel(object):
    # 代理获取的渠道
    page = 5
    proxy = set()
    refress_delay = 60 * 3600
    test_page = []
    start_urls = []
    page_generator = defaultdict(int)
    headers = None
    TIMEOUT = 20

    def next_page(self, url):
        yield url

    async def parse_page(self, session, url):
        text = await self.get(session, url)
        proxys = text >> to_doc >> extra_xpath("//table//tr[position()>1]")
        rst = []
        for proxy in proxys:
            host = proxy >> extra_xpath(
                "./td[position()=1]//text()") >> safe_extra
            port = proxy >> extra_xpath(
                "./td[position()=2]//text()") >> safe_extra
            rst.append((host, port))
        return rst

    @property
    def base_headers(self):
        return {
            'User-Agent': UserAgent().random
        }

    async def get(self, session, url, headers=None):
        headers = headers or self.base_headers
        proxy = DEBUG_PORXY if DEBUG_FLAG else None
        try:
            async with session.get(url, headers=headers, timeout=self.TIMEOUT, proxy=proxy, ssl=False) as res:
                return await res.text()
        except Exception:
            logger.error(url)
            logger.error(traceback.format_exc())
            return ''

    async def generate_start_urls(self, session):
        pass

    async def batch(self):
        tasks = []
        try:
            async with aiohttp.ClientSession() as session:
                if not self.start_urls:
                    self.start_urls = await self.generate_start_urls(session)
                for url in self.start_urls:
                    for page in self.next_page(url):
                        tasks.append(asyncio.ensure_future(
                            self.parse_page(session, page)))
                rst = await asyncio.gather(*tasks)
            return rst
        except Exception:
            logger.error(traceback.format_exc())
