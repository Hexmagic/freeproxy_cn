from freeproxy.core.channel import Channel


class IPHai(Channel):
    def __init__(self):
        Channel.__init__(self)
        self.funcmap = {self.parse_page: ['http://www.iphai.com/free/ng']}
