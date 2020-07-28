import aiohttp
from logzero import logger
from typing import List, Tuple
from freeproxy_cn.core.request import AsyncHttpHandler
from freeproxy_cn.util.pipe import head, to_doc, xpath, trim
from tqdm import tqdm


class Channel(object):
    site_name = 'site'
    start_urls: list = []  # 需要自己进行填充

    def __init__(self, debug=False, *arg, **kwargs):
        self.http_handler = AsyncHttpHandler()
        self.start_pos = 2
        self.positions = [1, 2]
        self.xpath_plt = './td[position()={}]//text()'

    async def bootstrap(self):
        return

    async def run(self):
        self.session = aiohttp.ClientSession()
        await self.bootstrap()
        rst = []
        for url in tqdm(self.start_urls, desc=f'{self.site_name} Grab'):
            proxies = await self.handle(url)
            rst += proxies
        await self.session.close()
        return rst

    async def handle(self, url: str) -> List[Tuple[str, str]]:
        try:
        doc = await self.http_handler.get(self.session, url,timeout=5) >> to_doc
            items = doc.xpath("//table//tr[position()>=%s]" % self.start_pos)
            proxies = []
            for item in items:
                host_position, port_position = self.positions
                host = item >> xpath(self.xpath_plt.format(
                    host_position)) >> head >> trim
                if not host:
                    # 匹配失败
                    continue
                port = item >> xpath(self.xpath_plt.format(
                    port_position)) >> head >> trim
                if len(port) > 5:
                    continue
                proxies.append((host, port))
            return proxies
        except:
            return []
