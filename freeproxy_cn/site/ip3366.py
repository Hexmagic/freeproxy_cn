from freeproxy_cn.core.channel import Channel


class Ip3366(Channel):
    def __init__(self, **kwargs):
        super(Ip3366, self).__init__(**kwargs)
        self.name = 'ip3366'
        self.url_plt = 'http://www.ip3366.net/?stype=1&page=%s'

    async def boostrap(self):
        urls = []
        for i in range(1, 11):
            urls.append(self.url_plt % i)
        self.funcmap = {self.handle: urls}
