from freeproxy.core.channel import Channel


class IPHai(Channel):
    def __init__(self):
        Channel.__init__(self)
        self.name = 'iphai'
        self.funcmap = {self.handle: ['http://www.iphai.com/free/ng']}
