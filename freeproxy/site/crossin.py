from freeproxy.core.channel import Channel
__all__ = ('Crossin')


class Crossin(Channel):
    def __init__(self):
        Channel.__init__(self)
        self.name = 'crossin'
        self.funcmap = {self.handle: ['http://lab.crossincode.com/proxy']}
