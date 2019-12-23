from freeproxy_cn.core.channel import Channel


class Xroxy(Channel):
    site_name = 'www.xproxy.com'
    start_urls = [
        'https://www.xroxy.com/free-proxy-lists/?port=&type=All_http&ssl=&country=CN&latency=&reliability=']

    def __init__(self, **kwargs):
        super(Xroxy, self).__init__(**kwargs)
