from freeproxy_cn.core.channel import Channel
from freeproxy_cn.util.pipe import to_doc
from typing import List, Tuple


class XiaoSu(Channel):
    site_name = 'www.xsdaili.com'

    def __init__(self, **kwargs):
        super(XiaoSu, self).__init__(**kwargs)

    async def bootstrap(self):
        content = await self.http_handler.get(self.session, "http://www.xsdaili.com/")
        doc = content >> to_doc
        suffixs = doc.xpath(
            '//div[@class="panel-body"]//div[@class="title"]/a/@href')[0:2]
        self.start_urls = [
            'http://www.xsdaili.com' + ele for ele in suffixs]

    async def handle(self,  url:str) -> List[Tuple[str, str]]:
        content = await self.http_handler.get(self.session, url)
        doc = content >> to_doc
        items = doc.xpath('//div[@class="cont"]/text()')
        proxies = []
        for item in items:
            item = item.strip('\r\n\t')
            if not item:
                continue
            [host, port] = item.strip().split('@')[0].split(':')
            proxies.append((host, port))
        return proxies
