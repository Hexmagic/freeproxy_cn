import asyncio
import aiohttp
from logzero import logger
from freeproxy.core.channel import Channel


class Engin(object):
    def __init__(self):
        self.sites = []

    def load_sites(self, site_clss):
        for clas in site_clss:
            self.sites.append(clas())

    async def _run(self):
        for site in self.sites:
            assert isinstance(site, Channel)
            async with aiohttp.ClientSession() as session:
                site.set_session(session)
                await site.boostrap()
                funcs = site.funcmap.keys()
                tasks = []
                for zp in zip(*site.funcmap.values()):
                    for func_param in zip(funcs, zp):
                        func, param = func_param
                        coro = func(param)
                        tasks.append(coro)
                await asyncio.gather(*tasks)

    async def run(self):
        while True:
            await self._run()
            await asyncio.sleep(60 * 60)
            logger.debug("开始新一轮的抓取")