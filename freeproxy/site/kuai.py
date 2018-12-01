from freeproxy.core.channel import Channel
from freeproxy.util.pipe import extra_xpath, extra_head, to_doc


class Kuai(Channel):
    LIMIT = 1
    REQUEST_DELAY = 2
    SYNC = True

    def __init__(self):
        Channel.__init__(self)
        self.funcmap = {
            self.parse_page: self.generator(
                'https://www.kuaidaili.com/free/intr/')+self.generator('https://www.kuaidaili.com/free/inha/')
        }

    def generator(self, url):
        rst, i = [], 0
        while i < self.PAGE:
            i += 1
            rst.append(url + '{}/'.format(i))
        return rst

    async def parse_page(self, session, url):
        text = await self.get(session, url)
        proxys = text >> to_doc >> extra_xpath("//table//tr[position()>1]")
        rst = []
        for proxy in proxys:
            host = proxy >> extra_xpath(
                "./td[position()=1]/text()") >> extra_head
            port = proxy >> extra_xpath(
                "./td[position()=2]/text()") >> extra_head
            rst.append((host, port))
        return rst
