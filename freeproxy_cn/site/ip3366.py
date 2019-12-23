from freeproxy_cn.core.channel import Channel


class Ip3366(Channel):
    site_name = 'www.ip3366.net'

    def __init__(self, **kwargs):
        super(Ip3366, self).__init__(**kwargs)
        self.url_plt = 'http://www.ip3366.net/?stype=1&page=%s'

    async def bootstrap(self):
        urls = []
        for i in range(1, 11):
            urls.append(self.url_plt % i)
        self.start_urls = urls
