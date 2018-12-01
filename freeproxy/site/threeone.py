import aiohttp

from freeproxy.core.channel import Channel
from freeproxy.util.pipe import extra_xpath, extra_head, to_doc


class ThreeOneF(Channel):
    def __init__(self):
        Channel.__init__(self)

    async def prepare(self, session):
        doc = await self.get(session, 'https://31f.cn/') >> to_doc
        hrefs = doc.xpath('//table[position()=2]//a/@href')
        hrefs = ['https://31f.cn' + ele for ele in hrefs]
        self.funcmap = {
            self.parse_page: hrefs
        }

    async def parse_page(self, session, url):
        proxys = await self.get(session, url) >> to_doc >> extra_xpath("//table[position()=1]//tr[position()>1]")
        rst = []
        for proxy in proxys:
            host = proxy >> extra_xpath(
                './td[position()=2]/text()') >> extra_head
            port = proxy >> extra_xpath(
                './td[position()=3]/text()') >> extra_head
            rst.append((host, port))
        return rst
