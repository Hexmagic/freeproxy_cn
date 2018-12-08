from freeproxy_cn.core.channel import Channel


class XiCi(Channel):
    def __init__(self):
        super(XiCi, self).__init__()
        self.name = "xici"
        self.url_plt = [
            "http://www.xicidaili.com/wn/%s",
            "http://www.xicidaili.com/wt/%s",
            "http://www.xicidaili.com/nn/%s",
            "http://www.xicidaili.com/nt/%s",
        ]

        self.td_idx = [2, 3]

    async def boostrap(self):
        urls = []
        for i in range(1, 3):
            urls += [plt % i for plt in self.url_plt]
        self.funcmap = {self.handle: urls}
