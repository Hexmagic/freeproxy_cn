from freeproxy_cn.core.channel import Channel
from freeproxy_cn.util.pipe import to_doc, xpath, head
from base64 import b64decode
import aiohttp
from typing import List, Tuple


class Cool(Channel):
    start_urls = [
        'https://www.cool-proxy.net/proxies/http_proxy_list/country_code:CN/port:/anonymous:']
    site_name = 'www.cool-proxy.net'

    def __init__(self, *args, **kwargs):
        super(Cool, self).__init__(*args, **kwargs)

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

    async def handle(self, url: str) -> List[Tuple[str, str]]:
        content = await self.http_handler.get(self.session, url)
        doc = content >> to_doc
        pro_lst = doc.xpath('//div[@id="main"]/table//tr[position()>1]')
        proxies = []
        for pro in pro_lst:
            ip_text = pro >> xpath('./td[position()=1]/script/text()') >> head
            if len(ip_text) <= 32:
                continue
            encode_host = ip_text.strip(')"').split('"')[-1]
            host = self.decode(encode_host)
            if not host:
                continue
            port = pro >> xpath('./td[position()=2]//text()') >> head
            proxies.append((host, port))
        return proxies
