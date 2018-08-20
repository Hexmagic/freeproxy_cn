from collections import defaultdict
import aiohttp
import asyncio
from fake_useragent import UserAgent


class Channel(object):
    # 代理获取的渠道
    page = 5
    proxy = set()
    refress_delay = 60 * 3600
    test_page = []
    start_urls = []
    page_generator = defaultdict(int)

    def next_page(self, url):
        yield url

    async def parse_page(self, session, url):
        pass

    async def get(self, session, url):
        async with session.get(url) as res:
            return await res.text()

    async def generate_start_urls(self):
        pass

    async def batch(self):
        tasks = []
        headers = {
            'User-Agent': UserAgent().random
        }
        rst = None
        
        async with aiohttp.ClientSession(headers=headers) as session:
            if not self.start_urls:
                self.start_urls = await self.generate_start_urls(session)
            for url in self.start_urls:
                for page in self.next_page(url):
                    tasks.append(asyncio.ensure_future(
                        self.parse_page(session, page)))
            rst = await asyncio.gather(*tasks)
        return rst
