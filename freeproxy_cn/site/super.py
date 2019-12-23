from freeproxy_cn.core.channel import Channel


class Super(Channel):
    site_name = 'www.superfastip.com'

    def __init__(self, **kwargs):
        super(Super, self).__init__(**kwargs)
        self.url_plt = 'http://www.superfastip.com/welcome/freeip/%s'

    async def bootstrap(self):
        self.start_urls = [self.url_plt % i for i in range(1, 5)]
