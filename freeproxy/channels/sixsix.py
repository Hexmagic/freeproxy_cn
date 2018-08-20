from freeproxy.channels import Channel
from freeproxy.util.pipe import to_doc, extra_xpath, safe_extra


class SixSix(Channel):
    start_urls = []

    async def generate_start_urls(self, session):
        proxy_urls = await self.get(session, 'http://www.66ip.cn/index.html') >> to_doc >> extra_xpath('//ul[@class="textlarge22"]/li[position()>1]/a/@href')
        return ['http://www.66ip.cn' + ele for ele in proxy_urls]

    async def parse_page(self, session, url):
        proxys = await self.get(session, url) >> to_doc >> extra_xpath("//table//tr[position()>1]")
        rst = []
        for proxy in proxys:
            host = proxy >> extra_xpath(
                "./td[position()=1]/text()") >> safe_extra
            port = proxy >> extra_xpath(
                "./td[position()=1]/text()") >> safe_extra
            rst.append([host, port])
        return rst
