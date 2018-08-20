from freeproxy.channels import Channel
from freeproxy.util.pipe import  to_doc, extra_xpath, safe_extra


class Kuai(Channel):
    start_urls = ['https://www.kuaidaili.com/free/intr/',
                  'https://www.kuaidaili.com/free/inha/']
    page = 5

    def next_page(self, url):
        while self.page_generator[url] < self.page:
            self.page_generator[url] += 1
            yield url + '{}/'.format(self.page_generator[url])

    async def parse_page(self, session, url):
        proxys = await self.get(session, url) >> to_doc >> extra_xpath("//table//tr[position()>1]")
        rst = []
        for proxy in proxys:
            host = proxy >> extra_xpath(
                "./td[position()=1]/text()") >> safe_extra
            port = proxy >> extra_xpath(
                "./td[position()=2]/text()") >> safe_extra
            rst.append([host, port])
        return rst
