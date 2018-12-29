import asyncio
import aiohttp
from logzero import logger
from freeproxy_cn.core.http import Http
from freeproxy_cn.site import CHAN1
from freeproxy_cn.site2 import CHAN2
import aredis


class Engin(object):
    def __init__(
        self,
        proxy_url=None,
        grab_hk=False,
        redis_host="127.0.0.1",
        redis_port=6379,
        redis_password="",
        redis_db=0,
    ):
        """
        proxy_url : 如要抓取香港代理需要设置代理
        grab_hk : 是否抓取香港代理，默认为false
        """
        self.name = "engin"
        self.rdm = aredis.StrictRedis(
            host=redis_host, port=redis_port, password=redis_password, db=redis_db
        )
        self.grab_hk = grab_hk
        self.proxy_url = proxy_url
        self.sites = self.load_default_sites()
        self.sem = asyncio.Semaphore(10)

    def load_default_sites(self):
        """
        加载默认抓取的代理网站
        """
        sites = []
        for clas in CHAN1:
            sites.append(clas())
        if self.grab_hk:
            for clas in CHAN2:
                sites.append(clas(self.proxy_url))
        return sites

    def set_site(self, sit):
        self.sites = [sit()]

    async def _run(self):
        tasks = []
        for site in self.sites:
            tasks.append(asyncio.ensure_future(self.site_run(site)))
        await asyncio.gather(*tasks)

    async def site_run(self, site):
        async with aiohttp.ClientSession() as session:
            site.set_http(Http(session))
            site.set_rdm(self.rdm)
            logger.debug("start grab site {}".format(site.name))
            await site.boostrap()
            funcs = site.funcmap.keys()
            for zp in zip(*site.funcmap.values()):
                for func_param in zip(funcs, zp):
                    async with self.sem:
                        func, param = func_param
                        coro = func(param)
                        await coro
                        await asyncio.sleep(2)  # 并发抓取 容易封禁ip

    async def run(self):
        while True:
            logger.debug("开始新一轮的抓取")
            await self._run()
            await asyncio.sleep(60 * 20)
