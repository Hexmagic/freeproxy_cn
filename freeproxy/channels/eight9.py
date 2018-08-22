from freeproxy.channels import Channel
from freeproxy.util.pipe import to_doc, extra_xpath, safe_extra


class Eight9(Channel):
    start_urls = [
        'http://www.89ip.cn/tqdl.html?api=1&num=1000&port=&address=&isp=']
    page = 3

    async def parse_page(self, session, url):
        proxies = await self.get(session, url) >> to_doc >> extra_xpath("//text()")
        rst = []
        for proxy in proxies[7:-1]:
            [host, port] = proxy.strip('\n\t\r ').split(':')
            rst.append((host, port))
        return rst
