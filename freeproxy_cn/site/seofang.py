from freeproxy_cn.core.channel import Channel


class SeoFang(Channel):
    site_name = 'ip.seofangfa.com'
    start_urls = ['http://ip.seofangfa.com/']

    def __init__(self, **kwargs):
        super(SeoFang, self).__init__(**kwargs)
