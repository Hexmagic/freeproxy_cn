from freeproxy_cn.core.channel import Channel
__all__ = ('Crossin')


class Crossin(Channel):
    def __init__(self, *args, **kwargs):
        super(Crossin, self).__init__(*args, **kwargs)
        self.name = 'crossin'
        self.funcmap = {self.handle: ['http://lab.crossincode.com/proxy']}
