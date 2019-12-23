from freeproxy_cn.core.channel import Channel
from freeproxy_cn.util.pipe import to_doc
from typing import List, Tuple


class Eight9(Channel):
    site_name = '89ip'
    start_urls = [
        'http://www.89ip.cn/tqdl.html?api=1&num=1000&port=&address=&isp=']

    def __init__(self, **kwargs):
        super(Eight9, self).__init__(**kwargs)

    async def handle(self, url: str) -> List[Tuple[str, str]]:
        content = await self.http_handler.get(self.session, url)
        doc = content >> to_doc
        items = doc.xpath('//body/text()')
        proxies = []
        for item in items[7:-1]:
            [host, port] = item.strip('\n\t\r ').split(':')
            proxies.append((host, port))
        return proxies
