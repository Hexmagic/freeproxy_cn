from freeproxy_cn.core.channel import Channel


class Super(Channel):
    def __init__(self):
        super(Super, self).__init__()
        self.name = 'super'
        self.url_plt = 'http://www.superfastip.com/welcome/freeip/%s'

    async def boostrap(self):
        self.funcmap = {
            self.handle: [self.url_plt % i for i in range(1, 5)]
        }
