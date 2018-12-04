from freeproxy_cn.core.channel import Channel
from freeproxy_cn.util.pipe import to_doc, extra_head
from base64 import b64decode


class Cool(Channel):
    def __init__(self, proxy=None):
        super(Cool, self).__init__()
        self.name = 'cool'
        self.funcmap = {
            self.handle_hk: [
                'https://www.cool-proxy.net/proxies/http_proxy_list/country_code:HK/port:/anonymous:'],
            self.handle_cn: [
                'https://www.cool-proxy.net/proxies/http_proxy_list/country_code:CN/port:/anonymous:'
            ]
        }

    def decode(self, text):
        tmp = []
        for al in list(text):
            if al == '=':
                tmp.append(al)
            elif str.isdigit(al):
                tmp.append(al)
            else:
                x = ord(al)
                if al.lower() < 'n':
                    z = x + 13
                else:
                    z = x - 13
                tmp.append(chr(z))
        encode_data = ''.join(tmp)
        try:
            return b64decode(encode_data).decode('utf8')
        except:
            return ''

    async def handle(self, url):
        content = await self.http.get(url)
        doc = content >> to_doc
        pro_lst = doc.xpath('//div[@id="main"]/table//tr[position()>1]')
        proxies = []
        for pro in pro_lst:
            ip_text = pro >> extra_head('./td[position()=1]/script/text()')
            if len(ip_text) <= 32:
                continue
            encode_host = ip_text.strip(')"').split('"')[-1]
            host = self.decode(encode_host)
            if not host:
                continue
            port = pro >> extra_head('./td[position()=2]//text()')
            proxies.append([host, port])
        return proxies

    async def handle_hk(self, url):
        proxies = await self.handle(url)
        await self.valid_google(proxies)

    async def handle_cn(self, url):
        proxies = await self.handle(url)
        await self.valid_ip(proxies)
