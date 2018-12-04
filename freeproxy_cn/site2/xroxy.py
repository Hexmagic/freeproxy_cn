from freeproxy_cn.core.channel import Channel
from freeproxy_cn.util.pipe import to_doc, extra_head


class Xroxy(Channel):
    def __init__(self, proxy=None):
        super(Xroxy, self).__init__()
        self.name = 'xroxy'
        self.funcmap = {
            self.handle_hk: [
                'https://www.xroxy.com/free-proxy-lists/?port=&type=All_http&ssl=&country=HK&latency=&reliability='],
            self.handle_cn: [
                'https://www.xroxy.com/free-proxy-lists/?port=&type=All_http&ssl=&country=CN&latency=&reliability=']
        }

    async def handle_hk(self, url):
        proxies = await self.handle(url)
        await self.valid_google(proxies)

    async def handle_cn(self, url):
        proxies = await self.handle(url)
        await self.valid_ip(proxies)
