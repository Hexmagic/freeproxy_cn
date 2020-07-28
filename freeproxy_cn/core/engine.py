import asyncio
import aiohttp
from logzero import logger
from freeproxy_cn.site import SITES
import redis
import threading
from operator import add
from functools import reduce
import aiohttp
from concurrent.futures import ThreadPoolExecutor
from freeproxy_cn.core.request import AsyncHttpHandler
from freeproxy_cn.util.pipe import split_into_n, slice_by
from typing import List, Tuple
from tqdm import tqdm


class Engin(object):
    def __init__(
        self,
        redis_host="127.0.0.1",
        redis_port=6379,
        redis_password="",
        valid_threads=4,
        valid_per_time=20,
        valid_url='http://icanhazip.com',
        valid_timeout=5,
        redis_db=0,
        sleep_time=20
    ):
        """
        param :
            redis_host: 存储代理的redis host
            redis_port: port
            valid_threads: 验证代理有效性的线程数目
            valid_per_time: 每次验证并发的url条数
            valid_url : 验证代理是否可用
            valid_timeout: 验证超时时间
        """
        self.name = "engin"
        self.vlaid_timeout = valid_timeout
        self.valid_url = valid_url
        self.sleep_time = sleep_time
        self.rdc = redis.StrictRedis(
            host=redis_host, port=redis_port, password=redis_password, db=redis_db
        )
        self.http_handler = AsyncHttpHandler(worker=valid_per_time)
        self.valid_threads = valid_threads
        self.valid_per_time = valid_per_time
        self._worker = ThreadPoolExecutor(max_workers=valid_threads)
        self.valid_timeout = valid_timeout
        self.cached = set()

    async def get_proxies(self):
        tasks = []
        for site in SITES:
            site_instance = site()
            tasks.append(asyncio.ensure_future(site_instance.run()))
        proxies = await asyncio.gather(*tasks)
        return list(reduce(add, proxies))

    async def valid_proxies(self, proxies: List[Tuple[str, str]]) -> List[Tuple[Tuple[str, str], bool]]:
        '''
        验证代理有效性 ，这里使用了多线程进行验证
        '''
        rtn: list = []
        for rst in self._worker.map(self.valid_job, proxies >> split_into_n(self.valid_threads)):
            rtn += rst
        return rtn

    def valid_job(self, proxies: List[Tuple[str, str]]) -> List[Tuple[Tuple[str, str], bool]]:
        '''
        每个线程内验证代理,需要自己申请eventloop
        '''
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        http_handler = AsyncHttpHandler()
        session = aiohttp.ClientSession()

        async def valid_proxy(proxy: Tuple[str, str]) -> Tuple[Tuple[str, str], bool]:
            '''
            验证代理有效性，这里只做了https的代理验证，这里我们已百度为目标
            '''
            host, port = proxy
            response = None
            try:
                response = await http_handler.get(session=session, url=self.valid_url, proxy=f'http://{host}:{port}', timeout=self.valid_timeout)
            except:
                return (proxy, False)
            if not response:
                return (proxy,False)
            return (proxy, True)

        async def _valid_job(proxies):
            rst: List = []
            thname = threading.current_thread().getName().split('_')[-1]            
            for proxy_list in tqdm(proxies >> slice_by(self.valid_per_time), desc=f"Valid Process {thname}"):
                tasks = [valid_proxy(proxy) for proxy in proxy_list]
                rst += await asyncio.gather(*tasks)
            return rst

        return loop.run_until_complete(_valid_job(proxies))

    def store(self, proxies: List[Tuple[Tuple[str, str], bool]]):
        '''
        存储到redis中，并删除无效的代理
        '''
        for proxy in proxies:
            proxy_tuple, valid = proxy
            host, port = proxy_tuple
            proxy_str = f'{host}:{port}'
            if not valid:
                if proxy_str in self.cached:
                    self.cached.remove(proxy_str)
                continue
            self.cached.add(proxy_str)
        logger.info(f"grab {len(self.cached)} valid proxies")
        # 直接清空可能会某一秒没有该key,重命名代价较小
        self.rdc.sadd('_https', *list(self.cached))
        self.rdc.rename('_https', self.valid_url)

    def site_list(self):
        for i, site in enumerate(SITES):
            print(f'[{i+1}]: {site.site_name}')

    async def run(self):
        while True:
            logger.debug(">>>>>>>>>>\nstart new grab process")
            proxies = await self.get_proxies()
            logger.info(f"\ngot {len(proxies)} proxies")
            logger.info("\n>>>>>>>>>>>\nstart valid proxies")
            proxies = await self.valid_proxies(proxies)
            self.store(proxies)
            await asyncio.sleep(60 * self.sleep_time)
