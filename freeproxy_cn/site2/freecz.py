from freeproxy_cn.core.channel import Channel
from freeproxy_cn.util.pipe import to_doc, extra_head
from base64 import b64decode


class freeproxy_cnCz(Channel):
    def __init__(self, proxy=None):
        super(freeproxy_cnCz, self).__init__()
        self.name = 'freeproxy_cn'
        self.funcmap = {
            self.handle_hk: [
                'http://free-proxy.cz/en/proxylist/country/HK/all/ping/all'],
            self.handle_cn: [
                'http://free-proxy.cz/en/proxylist/country/CN/all/ping/all'
            ]
        }

    async def handle(self, url):
        content = await self.http.get(url)
        doc = content >> to_doc
        pro_lst = doc.xpath('//table[@id="proxy_list"]//tr[position()>1]')
        proxies = []
        for pro in pro_lst:
            ip_text = pro >> extra_head('./td[position()=1]/script/text()')
            encode_host = ip_text.strip(')"').split('"')[-1]
            if len(encode_host) <= 32:
                continue
            host = b64decode(encode_host).decode('utf8')
            port = pro >> extra_head('./td[position()=2]//text()')
            proxies.append([host, port])
        return proxies

    async def handle_hk(self, url):
        proxies = await self.handle(url)
        await self.valid_google(proxies)

    async def handle_cn(self, url):
        proxies = await self.handle(url)
        await self.valid_ip(proxies)
