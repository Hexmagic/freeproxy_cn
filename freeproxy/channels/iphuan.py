from freeproxy.channels import Channel
from freeproxy.util.pipe import to_doc, extra_xpath, safe_extra
import re


class IPhuan(Channel):

    def __init__(self):
        super(IPhuan, self).__init__()
        self.pattern = re.compile(r'val\(\"[^"]*')
        self.funcmap = {
            self.parse_page: ['https://ip.ihuan.me/ti.html']
        }

    async def parse_page(self, session, url):
        text = await self.get(session, url)
        self.headers["Referer"] = 'https://ip.ihuan.me/ti.html'
        text = await self.get(session, 'https://ip.ihuan.me/mouse.do')
        val = self.pattern.search(text).group(0).replace('val("', '')
        data = {
            'num': 500,
            'port': '',
            'kill_port': '',
            'address': '',
            'kill_address': '',
            'anonymity': '',
            'type': '',
            'post': '',
            'sort': '',
            'key': val
        }
        self.headers['Origin'] = 'https://ip.ihuan.me'
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        text = await self.post(session, 'https://ip.ihuan.me/tqdl.html', data=data)
        proxys = text >> to_doc >> extra_xpath(
            '//div[@class="panel-body"]/text()')
        rst = []
        for proxy in proxys:
            try:
                host, port = (proxy >> safe_extra).split(':')
            except:
                continue
            rst.append((host, port))
        return rst
