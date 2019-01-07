from freeproxy_cn.core.channel import Channel


class Xroxy(Channel):
    def __init__(self, **kwargs):
        super(Xroxy, self).__init__(**kwargs)
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
