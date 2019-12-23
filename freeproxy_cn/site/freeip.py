from freeproxy_cn.core.channel import Channel
__all__ = ('FreeIP')


class FreeIP(Channel):
    site_name = 'www.freeip.top'
    start_urls = ['https://www.freeip.top/?page=1',
                  'https://www.freeip.top/?page=2']

    def __init__(self, *args, **kwargs):
        super(FreeIP, self).__init__(*args, **kwargs)
        self.positions = [1,2]