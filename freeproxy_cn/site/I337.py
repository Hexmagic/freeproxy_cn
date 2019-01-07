from freeproxy_cn.core.channel import Channel
from freeproxy_cn.util.pipe import to_doc, extra_head


class I337(Channel):
    def __init__(self, **kwargs):
        super(I337, self).__init__(**kwargs)
        self.name = 'i337'
        self.funcmap = {
            self.handle: ['https://proxy.l337.tech']
        }

    async def handle(self, url):
        content = await self.http.get(url)
        doc = content >> to_doc
        items = doc >> extra_head('//pre/text()')
        proxies = []
        for item in items.split('\n'):
            raw = item.strip('\r\t" ')
            if not raw:
                continue
            [host, port] = raw.split(':')
            proxies.append([host, port])
        await self.valid_ip(proxies)
