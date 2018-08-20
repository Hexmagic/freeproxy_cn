from collections import defaultdict


class Channel(object):
    # 代理获取的渠道
    page = 5
    http_proxy = defaultdict(set)
    https_proxy = defaultdict(set)
    refress_delay = 60 * 3600

    def __init__(self):
        pass
