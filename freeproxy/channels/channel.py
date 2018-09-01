import asyncio
from collections import defaultdict

import aiohttp
from fake_useragent import UserAgent

from freeproxy.util.db import getRedis
from freeproxy.util.log import get_trace, logger
from freeproxy.util.pipe import extra_host, extra_xpath, extra_head, to_doc


class Channel(object):
    __doc__ = '''
    example funcmap
    funcmap = {
        self.handle:[],
        self.hanle2:[]
    }

    if we want use proxy , we should create url_proxy_map to mentain url last proxy,so we cant report it when this proxy banned
    use sync to make http request sync ,and use request_delay to sleep
    '''
    funcmap = defaultdict(list)
    PAGE = 5  # max page crawl
    LIMIT = 10
    URL_PROXY_MAP = defaultdict(str)
    LOOP_DELAY = 60 * 10
    TIMEOUT = 20
    REQUEST_DELAY = 0
    SYNC = False
    RANDOM_PROXY = False  # use random proxy to guarantee not be baned
    rds = getRedis()

    def __init__(self):
        self.rdm = getRedis()
        self.headers = self.random_headers()

    def random_headers(self):
        return {'User-Agent': UserAgent().random}

    def get_loop(self):
        loop = asyncio.get_event_loop()
        return loop

    async def get(self, session, url, raw=False, binary=False, headers=None, proxy=None):
        '''
        session: request session
        url: should be http or https
        raw: return response obj or response text only
        headers: custom header
        proxy: custom proxy
        binary: return binary obj or yes
        '''
        headers = headers or self.headers
        try:
            if proxy and self.RANDOM_PROXY:
                self.URL_PROXY_MAP[url] = proxy
            headers['Host'] = url >> extra_host
            async with session.get(url, proxy=proxy, headers=headers, ssl=False) as res:
                if binary:
                    content = await res.read()
                else:
                    content = await res.text()
                return res if raw else content
        except Exception:
            logger.error(get_trace())
        return ''

    async def post(self, session, url, data=None, headers=None, json=None):
        '''
        session: request session
        url: should be http or https
        headers: custom header
        data: post data should be dict or urlencode string or tuple list
        json: should be dict
        '''
        headers = headers or self.headers
        async with session.post(
                url, headers=headers, data=data, ssl=False, json=json) as res:
            text = await res.text()
            return text

    async def prepare(self, session):
        '''
        do some thing before crawl , see xiaosu.py
        '''
        pass

    async def run(self):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=100, limit_per_host=self.LIMIT)) as session:
            await self.prepare(session)
            tasks = []
            if self.SYNC:
                rst = []
                for func, urls in self.funcmap.items():
                    for url in urls:
                        ele = await asyncio.gather(asyncio.ensure_future(func(session, url)))
                        rst += ele
                        await asyncio.sleep(self.REQUEST_DELAY)
                return rst
            else:
                for func, urls in self.funcmap.items():
                    for url in urls:
                        tasks.append(func(session, url))
                rst = await asyncio.gather(*tasks)
            return rst

    async def parse_page(self, session, url):
        text = await self.get(session, url)
        proxys = text >> to_doc >> extra_xpath("//table//tr[position()>1]")
        rst = []
        for proxy in proxys:
            host = proxy >> extra_xpath(
                "./td[position()=1]//text()") >> extra_head
            port = proxy >> extra_xpath(
                "./td[position()=2]//text()") >> extra_head
            rst.append((host, port))
        return rst
