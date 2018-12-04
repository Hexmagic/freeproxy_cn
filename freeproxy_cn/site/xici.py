from freeproxy_cn.core.channel import Channel


class XiCi(Channel):
    def __init__(self):
        super(XiCi, self).__init__()
        self.name = 'xici'
        self.wn_plt = 'http://www.xicidaili.com/wn/%s'
        self.wt_plt = 'http://www.xicidaili.com/wt/%s'
        self.td_idx = [2, 3]

    async def boostrap(self):
        urls = []
        for i in range(1, 3):
            urls.append(self.wn_plt % i)
            urls.append(self.wt_plt % i)
        self.funcmap = {
            self.handle: urls
        }
