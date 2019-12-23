from freeproxy_cn.core.channel import Channel
from freeproxy_cn.util.pipe import to_doc, xpath, trim
from typing import List, Tuple


class ProxyDocker(Channel):
    site_name = 'www.proxydocker.com'
    start_urls = ['https://www.proxydocker.com/en/proxylist/country/China']

    def __init__(self, **kwargs):
        super(ProxyDocker, self).__init__(**kwargs)

    async def handle(self, url: str) -> List[Tuple[str, str]]:
        content = await self.http_handler.get(self.session, url)
        doc = content >> to_doc
        pro_lst = doc.xpath(
            '//table[contains(@class,"proxylist_table")]//tr[position()>=1]')
        proxies = []
        for pro in pro_lst:
            href = pro >> xpath('./td/a/@href') >> trim
            if not href:
                continue
            [host, port] = href.split('/')[-1].split(':')
            proxies.append((host, port))
        return proxies
