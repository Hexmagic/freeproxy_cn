from freeproxy_cn.core.channel import Channel


class IPHai(Channel):
    site_name = 'www.iphai.com'
    start_urls = ['http://www.iphai.com/free/ng']

    def __init__(self, **kwargs):
        super(IPHai, self).__init__(**kwargs)
