from freeproxy_cn.core.channel import Channel
from freeproxy_cn.util.pipe import to_doc, extra_head


class Nova(Channel):
    def __init__(self, proxy=None):
        super(Nova, self).__init__()
        self.name = 'nova'
        self.funcmap = {
            self.handle_hk: [
                'https://www.proxynova.com/proxy-server-list/country-hk/'],
            self.handle_cn: [
                'https://www.proxynova.com/proxy-server-list/country-cn/']
        }

    async def handle(self, url):
        content = await self.http.get(url)
        doc = content >> to_doc
        pro_lst = doc.xpath('//table//tr[position()>1]')
        proxies = []
        for pro in pro_lst:
            ip_text = pro >> extra_head('.//abbr/script/text()')
            if not ip_text:
                continue
            ip_lst = ip_text.split("'")
            pre, suff = ip_lst[1], ip_lst[3]
            host = pre[8:]+suff
            port = pro >> extra_head('./td[position()=2]/a/text()')
            proxies.append([host, port])
        return proxies

    async def handle_hk(self, url):
        proxies = await self.handle(url)
        await self.valid_google(proxies)

    async def handle_cn(self, url):
        proxies = await self.handle(url)
        await self.valid_ip(proxies)
