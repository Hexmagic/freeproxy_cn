from freeproxy.core.channel import Channel


class IPJiang(Channel):
    def __init__(self):
        super(IPJiang, self).__init__()
        self.name = 'ipjiang'
        self.url_plt = 'http://ip.jiangxianli.com/?page=%s'
        self.td_idx = [2, 3]

    async def boostrap(self):
        urls = []
        for i in range(1, 26):
            urls.append(self.url_plt % i)
        self.funcmap = {
            self.handle: urls
        }
