from freeproxy_cn.core.channel import Channel


class SeoFang(Channel):

    def __init__(self, **kwargs):
        super(SeoFang, self).__init__(**kwargs)
        self.name = 'seofang'
        self.funcmap = {
            self.handle: ['http://ip.seofangfa.com/']
        }
