from freeproxy_cn.core.channel import Channel


class IPJiang(Channel):
    site_name = 'ip.jiangxianli.com'

    def __init__(self, **kwargs):
        super(IPJiang, self).__init__(**kwargs)
        self.url_plt = 'http://ip.jiangxianli.com/?page=%s'
        self.positions = [1, 2]

    async def bootstrap(self):
        urls = []
        for i in range(1, 26):
            urls.append(self.url_plt % i)
        self.start_urls = urls
