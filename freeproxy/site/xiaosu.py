import aiohttp

from freeproxy.core.channel import Channel
from freeproxy.util.pipe import extra_xpath, to_doc


class XiaoSu(Channel):
    start_urls = None

    def __init__(self):
        Channel.__init__(self)

    async def prepare(self, session):
        urls = await self.get(session, "http://www.xsdaili.com/") >> to_doc >> extra_xpath('//div[@class="panel-body"]//div[@class="title"]/a/@href')
        self.funcmap = {
            self.parse_page: ['http://www.xsdaili.com' + ele for ele in urls]
        }

    async def parse_page(self, session, url):
        proxys = await self.get(session, url) >> to_doc >> extra_xpath('//div[@class="cont"]/text()')
        rst = []
        for proxy in proxys:
            proxy = proxy.strip().split('@')[0]
            rst.append(tuple(proxy.split(":")))
        return rst
