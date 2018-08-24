from freeproxy.channels import Channel
from freeproxy.util.pipe import to_doc, extra_xpath, safe_extra


class XiCi(Channel):
    def __init__(self):
        Channel.__init__(self)
        self.funcmap = {
            self.parse_page: list(self.generate(
                'http://www.xicidaili.com/wn/'))+list(self.generate('http://www.xicidaili.com/wt/'))
        }

    def generate(self, url):
        i = 0
        while i < self.PAGE:
            i += 1
            yield url + str(i)

    async def parse_page(self, session, url):
        proxys = await self.get(session, url) >> to_doc >> extra_xpath(
            '//table[@id="ip_list"]//tr[position()>1]')
        rst = []
        for proxy in proxys:
            host = proxy >> extra_xpath(
                './/td[position()=2]/text()') >> safe_extra
            port = proxy >> extra_xpath(
                './/td[position()=3]/text()') >> safe_extra
            rst.append((host, port))
        return rst
