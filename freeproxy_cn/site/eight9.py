from freeproxy_cn.core.channel import Channel
from freeproxy_cn.util.pipe import to_doc


class Eight9(Channel):
    def __init__(self, **kwargs):
        Channel.__init__(self, **kwargs)
        self.name = 'eight9'
        self.funcmap = {
            self.handle: [
                'http://www.89ip.cn/tqdl.html?api=1&num=1000&port=&address=&isp='
            ]
        }

    async def handle(self, url):
        content = await self.http.get(url)
        doc = content >> to_doc
        items = doc.xpath('//body/text()')
        proxies = []
        for item in items[7:-1]:
            [host, port] = item.strip('\n\t\r ').split(':')
            proxies.append([host, port])
        await self.valid_ip(proxies)
