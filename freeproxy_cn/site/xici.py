from freeproxy_cn.core.channel import Channel


class XiCi(Channel):
    site_name = 'www.xicidaili.com'

    def __init__(self, **kwargs):
        super(XiCi, self).__init__(**kwargs)
        self.name = "xici"
        self.url_plt = [
            "http://www.xicidaili.com/wn/%s",
            "http://www.xicidaili.com/wt/%s",
            "http://www.xicidaili.com/nn/%s",
            "http://www.xicidaili.com/nt/%s",
        ]

        self.positions = [2, 3]

    async def bootstrap(self):
        urls = []
        for i in range(1, 3):
            urls += [plt % i for plt in self.url_plt]
        self.start_urls = urls
