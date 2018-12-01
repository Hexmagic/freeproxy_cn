from freeproxy.core.channel import Channel
from freeproxy.util.pipe import to_doc, extra_xpath


class Eight9(Channel):
    PAGE = 3

    def __init__(self):
        Channel.__init__(self)
        self.funcmap = {
            self.parse_page: [
                'http://www.89ip.cn/tqdl.html?api=1&num=1000&port=&address=&isp='
            ]
        }

    async def parse_page(self, session, url):
        proxies = await self.get(session,
                                 url) >> to_doc >> extra_xpath("//text()")
        rst = []
        for proxy in proxies[7:-1]:
            [host, port] = proxy.strip('\n\t\r ').split(':')
            rst.append((host, port))
        return rst
