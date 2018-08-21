from freeproxy.channels import Channel
from freeproxy.util.pipe import to_doc, extra_xpath, safe_extra
import aiohttp
import asyncio


class Kuai(Channel):
    start_urls = ['https://www.kuaidaili.com/free/intr/',
                  'https://www.kuaidaili.com/free/inha/']
    page = 5

    def next_page(self, url):
        while self.page_generator[url] < self.page:
            self.page_generator[url] += 1
            yield url + '{}/'.format(self.page_generator[url])

    async def parse_page(self, session, url):
        text = await self.get(session, url)
        proxys = text >> to_doc >> extra_xpath("//table//tr[position()>1]")
        rst = []
        for proxy in proxys:
            host = proxy >> extra_xpath(
                "./td[position()=1]/text()") >> safe_extra
            port = proxy >> extra_xpath(
                "./td[position()=2]/text()") >> safe_extra
            rst.append((host, port))
        return rst

    async def batch(self):
        rst = []
        async with aiohttp.ClientSession() as session:
            if not self.start_urls:
                self.start_urls = await self.generate_start_urls(session)
            for url in self.start_urls:
                for page in self.next_page(url):
                    rst.append(await asyncio.ensure_future(
                        self.parse_page(session, page)))
                    await asyncio.sleep(1)
        return rst
