from freeproxy.channels import Channel
from freeproxy.util.pipe import to_doc, extra_xpath
import aiohttp


class XiaoSu(Channel):
    start_urls = None

    def __init__(self):
        Channel.__init__(self)
        self.funcmap = {
            self.parse_page: self.generate()
        }

    def generate(self):
        loop = self.get_loop()
        rst = loop.run_until_complete(self.generate_start_urls())
        return rst

    async def generate_start_urls(self):
        async with aiohttp.ClientSession() as session:
            urls = await self.get(session, "http://www.xsdaili.com/") >> to_doc >> extra_xpath('//div[@class="panel-body"]//div[@class="title"]/a/@href')
            return ['http://www.xsdaili.com' + ele for ele in urls]

    async def parse_page(self, session, url):
        proxys = await self.get(session, url) >> to_doc >> extra_xpath('//div[@class="cont"]/text()')
        rst = []
        for proxy in proxys:
            proxy = proxy.strip().split('@')[0]
            rst.append(tuple(proxy.split(":")))
        return rst
