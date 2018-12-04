from freeproxy_cn.core.channel import Channel
from freeproxy_cn.util.pipe import to_doc


class XiaoSu(Channel):
    def __init__(self):
        super(XiaoSu, self).__init__()
        self.name = 'xiaosu'

    async def boostrap(self):
        content = await self.http.get("http://www.xsdaili.com/")
        doc = content >> to_doc
        suffixs = doc.xpath(
            '//div[@class="panel-body"]//div[@class="title"]/a/@href')[0:2]
        self.funcmap = {
            self.handle: [
                'http://www.xsdaili.com' + ele for ele in suffixs]
        }

    async def handle(self,  url):
        content = await self.http.get(url)
        doc = content >> to_doc
        items = doc.xpath('//div[@class="cont"]/text()')
        proxies = []
        for item in items:
            item = item.strip('\r\n\t')
            if not item:
                continue
            [host, port] = item.strip().split('@')[0].split(':')
            proxies.append([host, port])
        await self.valid_ip(proxies)
