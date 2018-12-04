from freeproxy_cn.core.channel import Channel
from freeproxy_cn.util.pipe import to_doc, extra_head


class Idcloak(Channel):
    def __init__(self, proxy=None):
        super(Idcloak, self).__init__()
        self.name = 'idcloak'
        self.funcmap = {
            self.handle_hk: [
                'http://www.idcloak.com/proxylist/proxy-list.html?country=HK&port%5B%5D=all&protocol-http=true&protocol-https=true&anonymity-low=true&anonymity-medium=true&anonymity-high=true&connection-low=true&connection-medium=true&connection-high=true&speed-low=true&speed-medium=true&speed-high=true&order=desc&by=updated'],
            self.handle_cn: [
                'http://www.idcloak.com/proxylist/proxy-list.html?country=CN&port%5B%5D=all&protocol-http=true&protocol-https=true&anonymity-low=true&anonymity-medium=true&anonymity-high=true&connection-low=true&connection-medium=true&connection-high=true&speed-low=true&speed-medium=true&speed-high=true&order=desc&by=updated']
        }

    async def handle(self, url):
        content = await self.http.get(url)
        doc = content >> to_doc
        pro_lst = doc.xpath('//table//tr[position()>1]')
        proxies = []
        for pro in pro_lst:
            port = pro >> extra_head('//td[position()=7]/text()')
            host = pro >> extra_head('//td[position()=8]/text()')
            proxies.append([host, port])
        return proxies

    async def handle_hk(self, url):
        proxies = await self.handle(url)
        await self.valid_google(proxies)

    async def handle_cn(self, url):
        proxies = await self.handle(url)
        await self.valid_ip(proxies)
