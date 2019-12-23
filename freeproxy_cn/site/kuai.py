from freeproxy_cn.core.channel import Channel


class Kuai(Channel):
    site_name = 'www.kuaidaili.com'
    start_urls = ['https://www.kuaidaili.com/free/intr/',
                  'https://www.kuaidaili.com/free/inha/']

    def __init__(self, **kwargs):
        super(Kuai, self).__init__(**kwargs)
        self.positions = [1, 2]
