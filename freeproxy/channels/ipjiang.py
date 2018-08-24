from freeproxy.channels import Channel
from freeproxy.util.pipe import to_doc, extra_xpath, safe_extra


class IPJiang(Channel):
    PAGE = 28

    def __init__(self):
        Channel.__init__(self)
        self.funcmap = {
            self.parse_page: self.generator(
                'http://ip.jiangxianli.com/?page={}')
        }

    def generator(self, url):
        i = 0
        rst = []
        while i < self.PAGE:
            i += 1
            rst.append(url.format(i))
        return rst

    async def parse_page(self, session, url):
        text = await self.get(session, url)
        proxys = text >> to_doc >> extra_xpath("//table//tr[position()>1]")
        rst = []
        for proxy in proxys:
            host = proxy >> extra_xpath(
                "./td[position()=2]//text()") >> safe_extra
            port = proxy >> extra_xpath(
                "./td[position()=3]//text()") >> safe_extra
            rst.append((host, port))
        return rst
