from freeproxy_cn.core.channel import Channel
from freeproxy_cn.util.pipe import to_doc, extra_head


class ProxyDocker(Channel):
    def __init__(self, **kwargs):
        super(ProxyDocker, self).__init__(**kwargs)
        self.name = 'proxydocker'
        self.funcmap = {
            self.handle_hk: [
                'https://www.proxydocker.com/en/proxylist/country/Hong%20Kong'],
            self.handle_cn: [
                'https://www.proxydocker.com/en/proxylist/country/China'
            ]
        }

    async def handle(self, url):
        content = await self.http.get(url)
        doc = content >> to_doc
        pro_lst = doc.xpath(
            '//table[contains(@class,"proxylist_table")]//tr[position()>=1]')
        proxies = []
        for pro in pro_lst:
            href = pro >> extra_head('./td/a/@href')
            if not href:
                continue
            [host, port] = href.split('/')[-1].split(':')
            proxies.append([host, port])
        return proxies

    async def handle_hk(self, url):
        proxies = await self.handle(url)
        await self.valid_google(proxies)

    async def handle_cn(self, url):
        proxies = await self.handle(url)
        await self.valid_ip(proxies)
