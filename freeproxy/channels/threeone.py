import aiohttp

from freeproxy.channels import Channel
from freeproxy.util.pipe import extra_xpath, safe_extra, to_doc


class ThreeOneF(Channel):
    def __init__(self):
        Channel.__init__(self)
        self.funcmap = {
            self.parse_page: self.generator('https://31f.cn/')
        }

    def generator(self, url):
        loop = self.get_loop()
        rst = loop.run_until_complete(self.generator_url(url))
        return rst

    async def generator_url(self, url):
        async with aiohttp.ClientSession() as session:
            doc = await self.get(session, url) >> to_doc
            hrefs = doc.xpath('//table[position()=2]//a/@href')
            hrefs = ['https://31f.cn' + ele for ele in hrefs]
            return hrefs
            
    async def parse_page(self, session, url):
        proxys = await self.get(session, url) >> to_doc >> extra_xpath("//table[position()=1]//tr[position()>1]")
        rst = []
        for proxy in proxys:
            host = proxy >> extra_xpath(
                './td[position()=2]/text()') >> safe_extra
            port = proxy >> extra_xpath(
                './td[position()=3]/text()') >> safe_extra
            rst.append((host, port))
        return rst
