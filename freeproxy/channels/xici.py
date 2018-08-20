from freeproxy.channels import Channel
from freeproxy.util.pipe import to_str, to_doc, extra_xpath, to_proxy, safe_extra


class XiCi(Channel):
    start_urls = ['http://www.xicidaili.com/wn/',
                  'http://www.xicidaili.com/wt/']

    def next_page(self, url):
        while self.page_generator[url] < self.page:
            self.page_generator[url] += 1
            yield url + self.page_generator >> to_str

    def parse_page(self, session, url):
        proxys = url >> to_doc >> extra_xpath(
            '//table[@id="ip_list"]//tr[position()>1]')
        for proxy in proxys:
            host = proxy >> extra_xpath(
                './/td[position()=1]/text()') >> safe_extra
            port = proxy >> extra_xpath(
                './/td[position()=2]/text()') >> safe_extra
            self.proxy.add((host, port) >> to_proxy)
