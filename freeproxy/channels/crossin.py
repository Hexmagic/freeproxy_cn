from freeproxy.channels import Channel
__all__ = ('Crossin')


class Crossin(Channel):
    def __init__(self):
        Channel.__init__(self)
        self.funcmap = {
            self.parse_page: ['http://lab.crossincode.com/proxy']
        }
