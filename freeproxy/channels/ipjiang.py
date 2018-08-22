from freeproxy.channels import Channel
from freeproxy.util.pipe import to_doc, extra_xpath, safe_extra


class IPJiang(Channel):
    start_urls = ['http://ip.jiangxianli.com/?page={}']
    page = 28

    def next_page(self, url):
        while self.page_generator[url] < self.page:
            self.page_generator[url] += 1
            yield self.start_urls[0].format(self.page_generator)

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
