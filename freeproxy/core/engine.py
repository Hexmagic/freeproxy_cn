import asyncio
import aiohttp
from logzero import logger
from freeproxy.core.http import Http
from freeproxy.config import REDIS_DB, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT
import aredis


class Engin(object):
    def __init__(self):
        self.name = 'engin'
        self.rdm = aredis.StrictRedis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=REDIS_DB
        )

    def set_site(self, site_cls):
        self.site = site_cls()

    async def _run(self):
        site = self.site
        async with aiohttp.ClientSession() as session:
            site.set_http(Http(session))
            site.set_rdm(self.rdm)
            await site.boostrap()
            funcs = site.funcmap.keys()
            for zp in zip(*site.funcmap.values()):
                for func_param in zip(funcs, zp):
                    func, param = func_param
                    coro = func(param)
                    await coro
                    await asyncio.sleep(2)  # 并发抓取 容易封禁ip

    async def run(self):
        while True:
            await self._run()
            await asyncio.sleep(60 * 60)
            logger.debug("开始新一轮的抓取")
