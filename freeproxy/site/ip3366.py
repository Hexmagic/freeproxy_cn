from freeproxy.core.channel import Channel


class Ip3366(Channel):
    PAGE = 10
    TIMEOUT = 50

    def __init__(self):
        Channel.__init__(self)
        self.funcmap = {self.parse_page: self.generator()}

    def generator(self):
        rst, i = [], 0
        while i < self.PAGE:
            i += 1
            rst.append('http://www.ip3366.net/?stype=1&page={}'.format(i))
        return rst
