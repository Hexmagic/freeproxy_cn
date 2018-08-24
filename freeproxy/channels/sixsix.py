from freeproxy.channels import Channel
from freeproxy.util.pipe import to_doc, extra_xpath
import random


class SixSix(Channel):
    LOOP_DELAY = random.choice([5, 6, 7])

    def __init__(self):
        Channel.__init__(self)
        self.funcmap = {
            self.parse_page: [
                'http://www.66ip.cn/nmtq.php?getnum=300&isp=0&anonymoustype=2&start=&ports=&export=&ipaddress=&area=1&proxytype=1&api=66ip']
        }

    async def parse_page(self, session, url):
        text = await self.get(session, url)
        proxys = text >> to_doc >> extra_xpath("//body//text()")
        rst = []
        for proxy in proxys[:-10]:
            proxy = proxy.strip('" \t\r\n')
            [host, port] = proxy.split(':')
            rst.append((host, port))
        return rst
