from collections import defaultdict
from freeproxy_cn.util.pipe import to_doc, extra_head
from freeproxy_cn.core.http import Http
from cuckoopy import CuckooFilter
from logzero import logger
import aredis
import asyncio


class Channel(object):
    def __init__(self, proxy=None, *arg, **kwargs):
        self.funcmap = defaultdict()
        self.http = Http()
        self.rdm = aredis.StrictRedis  # 这两行是为了代码提示，实际情况会由外部设置
        self.proxy = proxy
        self.name = 'channel'
        self.start_pos = 2
        self.td_idx = [1, 2]
        self.bucket = CuckooFilter(
            capacity=1000, bucket_size=4, fingerprint_size=1)

    async def boostrap(self):
        pass

    def set_http(self, http):
        self.http = http
        self.http.proxy = self.proxy

    def set_rdm(self, rdm):
        self.rdm = rdm

    async def store_http_proxies(self, proxies):
        logger.info("{} grab {} valid http proxies".format(
            self.name, len(proxies)))
        new_proxies = []
        for p in proxies:
            if self.bucket.contains(p):
                continue
            else:
                try:
                    self.bucket.insert(p)
                except Exception:
                    self.bucket = CuckooFilter()
                new_proxies.append(p)
        await self.rdm.lpush('http', *new_proxies)

    async def store_https_proxies(self, proxies):
        logger.info("{} grab {} valid https proxies".format(
            self.name, len(proxies)))
        new_proxies = []
        for p in proxies:
            if self.bucket.contains(p):
                continue
            else:
                try:
                    self.bucket.insert(p)
                except Exception:
                    self.bucket = CuckooFilter()
                new_proxies.append(p)
        await self.rdm.lpush('http', *new_proxies)

    async def store_google(self, proxies):
        logger.info("{} grab {} valid google proxies".format(
            self.name, len(proxies)))
        new_proxies = []
        for p in proxies:
            if self.bucket.contains(p):
                continue
            else:
                try:
                    self.bucket.insert(p)
                except Exception:
                    self.bucket = CuckooFilter()
                new_proxies.append(p)
        await self.rdm.lpush('http', *new_proxies)

    async def valid_google(self, proxies):
        if not proxies:
            return
        valid_google = await self.valid_url('https://www.google.com', proxies)
        if valid_google:
            await self.store_google(valid_google)

    async def valid_ip(self, proxies):
        valid_http = await self.valid_url('http://www.httpbin.org/', proxies)
        valid_https = await self.valid_url('https://www.ip.cn', proxies)
        if valid_http:
            await self.store_http_proxies(valid_http)
        if valid_https:
            await self.store_https_proxies(valid_https)

    async def valid_url(self, url: str, proxies: list):
        tasks, pro_lst = [], []
        if not proxies:
            return
        for proxy in proxies:
            if not proxy[0] or not proxy[1]:
                continue
            proxy = 'http://{}:{}'.format(*proxy)
            tasks.append(asyncio.ensure_future(self.http.get(
                'http://www.httpbin.org/', proxy=proxy, raw=True)))
        responses = await asyncio.gather(*tasks)
        for ix, response in enumerate(responses):
            if response:
                if response.status == 200:
                    pro_lst.append(':'.join(proxies[ix]))
        return pro_lst

    async def handle(self, url):
        doc = await self.http.get(url) >> to_doc
        items = doc.xpath("//table//tr[position()>=%s]" % self.start_pos)
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
        await self.valid_ip(proxies)
