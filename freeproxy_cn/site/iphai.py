from freeproxy_cn.core.channel import Channel


class IPHai(Channel):
    def __init__(self, **kwargs):
        Channel.__init__(self, **kwargs)
        self.name = 'iphai'
        self.funcmap = {self.handle: ['http://www.iphai.com/free/ng']}
