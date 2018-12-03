from collections import defaultdict
from freeproxy.util.pipe import to_doc, extra_head
from freeproxy.core.http import Http
from logzero import logger
import aredis


class Channel(object):
    def __init__(self):
        self.funcmap = defaultdict()
        self.http = Http()
        self.rdm = aredis.StrictRedis  # 这两行是为了代码提示，实际情况会由外部设置
        self.name = 'channel'
        self.td_idx = [1, 2]

    async def boostrap(self):
        pass

    def set_http(self, http):
        self.http = http

    def set_rdm(self, rdm):
        self.rdm = rdm

    async def store_proxies(self, proxies):
        logger.info("{} grab {} proxies".format(self.name, len(proxies)))
        logger.info("top 5 proxy {} ".format(proxies[:5]))

    async def handle(self, url):
        doc = await self.http.get(url) >> to_doc
        items = doc.xpath("//table//tr[position()>1]")
        proxies = []
        for item in items:
            try:
                host = item >> extra_head(
                    "./td[position()=%s]//text()" % self.td_idx[0])
                port = item >> extra_head(
                    "./td[position()=%s]//text()" % self.td_idx[1])
            except Exception:
                continue
            if len(port) > 5:
                continue
            proxies.append((host, port))
        await self.store_proxies(proxies)
