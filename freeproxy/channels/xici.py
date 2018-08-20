from freeproxy.channels import Channel
from freeproxy.util.pipe import to_str, to_doc, extra_xpath, safe_extra


class XiCi(Channel):
    start_urls = ['http://www.xicidaili.com/wn/',
                  'http://www.xicidaili.com/wt/']

    def next_page(self, url):
        while self.page_generator[url] < self.page:
            self.page_generator[url] += 1
            yield url + (self.page_generator[url] >> to_str)

    async def parse_page(self, session, url):
        proxys = await self.get(session, url) >> to_doc >> extra_xpath(
            '//table[@id="ip_list"]//tr[position()>1]')
        rst = []
        for proxy in proxys:
            host = proxy >> extra_xpath(
                './/td[position()=2]/text()') >> safe_extra
            port = proxy >> extra_xpath(
                './/td[position()=3]/text()') >> safe_extra
            rst.append([host, port])
        return rst
