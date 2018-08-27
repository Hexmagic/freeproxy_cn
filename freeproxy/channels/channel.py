import asyncio
from collections import defaultdict

import aiohttp
from fake_useragent import UserAgent

from freeproxy.util.db import getRedis
from freeproxy.util.log import get_trace, logger
from freeproxy.util.pipe import extra_host, extra_xpath, safe_extra, to_doc
from information.conf import DEBUG_PROXY, DEBUG_SYMBOL, PROXY_KEY


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
    URL_PROXY_MAP = {}
    LOOP_DELAY = 60 * 10
    TIMEOUT = 20
    REQUEST_DELAY = 0
    SYNC = False
    RANDOM_PROXY = False  # use random proxy to guarantee not be baned
    rds = getRedis()

    def __init__(self):
        self.rdm = getRedis()
        self.headers = self.random_headers()
        self.proxy = DEBUG_PROXY if DEBUG_SYMBOL else None

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
        proxy = getattr(self, 'proxy', proxy) or await self.fetch_proxy() if self.RANDOM_PROXY else None
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
        except aiohttp.ClientProxyConnectionError:
            logger.warning("proxy {} connnect error".format(proxy))
            return await self.report_proxy(session, url)
        except aiohttp.ClientHttpProxyError:
            logger.warning("proxy {} connnect error".format(proxy))
            return await self.report_proxy(session, url)
        except aiohttp.ServerDisconnectedError as e:
            if not e.message:
                logger.warning("get empty error with not msg {}".format(e))
                return await self.report_proxy(session, url)
            if e.message.code == 429:
                logger.warning(
                    "proxy {} too mmany  connnect errot".format(proxy))
                return await self.report_proxy(session, url)
        except aiohttp.client_exceptions.ClientOSError:
            logger.warning(
                "connection {} closed by remote host ".format(proxy))
            await asyncio.sleep(self.REQUEST_DELAY)
            return await self.report_proxy(session, url)
        except Exception:
            logger.error(get_trace())
        return ''

    async def report_proxy(self, session, url):
        proxy = self.URL_PROXY_MAP[url]
        logger.warning("proxy {} banned ".format(proxy))
        await self.rdm.srem(PROXY_KEY, proxy)
        proxy = await self.fetch_proxy()
        return await self.get(session, url, proxy=proxy)

    async def fetch_proxy(self):
        rst = await self.rds.srandmember(PROXY_KEY, 1)
        if not rst:
            return None
        else:
            return rst[0].decode('utf8')

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

    async def prpare(self, session):
        '''
        do some thing before crawl , see xiaosu.py
        '''
        pass

    async def run(self):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=100, limit_per_host=self.LIMIT)) as session:
            await self.prpare(session)
            tasks = []
            if self.SYNC:
                rst = []
                logger.info("request performed sync")
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
                "./td[position()=1]//text()") >> safe_extra
            port = proxy >> extra_xpath(
                "./td[position()=2]//text()") >> safe_extra
            rst.append((host, port))
        return rst
