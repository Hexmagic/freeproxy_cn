from freeproxy_cn.core.channel import Channel
__all__ = ('Crossin')


class Crossin(Channel):
    site_name = 'lab.crossincode.com'
    start_urls = ['http://lab.crossincode.com/proxy']

    def __init__(self, *args, **kwargs):
        super(Crossin, self).__init__(*args, **kwargs)
