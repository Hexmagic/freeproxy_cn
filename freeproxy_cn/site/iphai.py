from freeproxy_cn.core.channel import Channel


class IPHai(Channel):
    def __init__(self, **kwargs):
        super(IPHai, self).__init__(**kwargs)
        self.name = 'iphai'
        self.funcmap = {self.handle: ['http://www.iphai.com/free/ng']}
