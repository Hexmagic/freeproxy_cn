from freeproxy_cn.core.channel import Channel
from freeproxy_cn.util.pipe import to_doc


class MyProxy(Channel):
    def __init__(self, proxy=None):
        super(MyProxy, self).__init__()
        self.name = 'myproxy'
        self.url_plt = 'https://www.my-proxy.com/free-proxy-list-%s.html'

    async def boostrap(self):
        urls = []
        for i in range(1, 11):
            urls.append(self.url_plt % i)
        self.funcmap = {
            self.handle: [urls]
        }

    async def handle_cn(self, url):
        content = await self.http.get(url)
        doc = content >> to_doc
        proxies = []
        items = doc.xpath('//div[@class="list"]/text()')
        for item in items:
            hp, area = item.split('#')
            if area != 'CN':
                continue
            [host, port] = hp.split(':')
            proxies.append([host, port])
        items = doc.xpath('//div[contains(@class,"onp-sl-content")]/text()')
        for item in items:
            hp, area = item.split('#')
            if area != 'CN':
                continue
            [host, port] = hp.split(':')
            proxies.append([host, port])
        await self.valid_ip(proxies)
