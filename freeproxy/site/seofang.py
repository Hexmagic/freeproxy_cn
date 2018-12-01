from freeproxy.core.channel import Channel


class SeoFang(Channel):

    def __init__(self):
        Channel.__init__(self)
        self.funcmap = {
            self.parse_page: ['http://ip.seofangfa.com/']
        }
