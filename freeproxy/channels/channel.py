from collections import defaultdict
import aiohttp
import asyncio


class Channel(object):
    # 代理获取的渠道
    page = 5
    proxy = set()
    refress_delay = 60 * 3600
    test_page = []
    start_urls = []
    page_generator = defaultdict(int)

    def next_page(self, url):
        pass

    async def parse_page(self, session, url):
        pass

    async def batch(self):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for url in self.start_urls:
                for page in self.next_page(url):
                    tasks.append(self.parse_page(session, page))
        return await asyncio.gather(*tasks)
