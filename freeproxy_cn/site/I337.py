from freeproxy_cn.core.channel import Channel
from freeproxy_cn.util.pipe import to_doc, xpath,head
from typing import List, Tuple


class I337(Channel):
    site_name = 'proxy.l337.tech'
    start_urls = ['https://proxy.l337.tech']

    def __init__(self, **kwargs):
        super(I337, self).__init__(**kwargs)

    async def handle(self, url: str) -> List[Tuple[str, str]]:
        content = await self.http_handler.get(self.session, url)
        doc = content >> to_doc
        items = doc >> xpath('//pre/text()')>>head
        proxies = []
        for item in items.split('\n'):
            raw = item.strip('\r\t" ')
            if not raw:
                continue
            [host, port] = raw.split(':')
            proxies.append((host, port))
        return proxies
