from collections import defaultdict
from freeproxy.util.pipe import to_doc, extra_head


class Channel(object):
    def __init__(self):
        self.funcmap = defaultdict()

    async def boostrap(self):
        pass

    def set_session(self):
        pass

    async def parse_page(self, session, url):
        doc = await self.get(session, url) >> to_doc
        proxys = doc.xpath("//table//tr[position()>1]")
        rst = []
        for proxy in proxys:
            host = proxy >> extra_head("./td[position()=1]//text()")
            port = proxy >> extra_head("./td[position()=2]//text()")
            rst.append((host, port))
        return rst