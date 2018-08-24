from freeproxy.channels import Channel
from freeproxy.util.pipe import to_doc, extra_xpath, safe_extra


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
        loop = self.get_loop()
        rst = loop.run_until_complete(self.page_generator(url))
        return rst

    async def page_generator(self, url):
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
                "./td[position()=1]/text()") >> safe_extra
            port = proxy >> extra_xpath(
                "./td[position()=2]/text()") >> safe_extra
            rst.append((host, port))
        return rst
