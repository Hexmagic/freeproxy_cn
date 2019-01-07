from freeproxy_cn.core.channel import Channel


class Kuai(Channel):
    def __init__(self, **kwargs):
        super(Kuai, self).__init__(**kwargs)
        self.name = 'kuai'
        self.funcmap = {
            self.handle: ['https://www.kuaidaili.com/free/intr/',
                          'https://www.kuaidaili.com/free/inha/']
        }
        self.td_idx = [1, 2]
