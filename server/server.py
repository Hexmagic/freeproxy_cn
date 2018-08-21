import asyncio
import itertools
import traceback
from concurrent.futures import ThreadPoolExecutor

import aredis
from aiohttp import web

from config import PROXY_KEY, REDIS_DB, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT
from freeproxy.channels import CHANS, Channel
from freeproxy.model import Proxy
from freeproxy.util.log import logger




async def get_proxy(request):
    return web.json_response({"ac": "bd"})


class Application(web.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)


async def grab_and_store(channel):
    assert issubclass(channel, Channel), "Not support Class"
    client = aredis.StrictRedis(
        host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)
    coro = channel().batch()
    proxy_list = await asyncio.gather(coro)
    unique = set(list(itertools.chain(*itertools.chain(*proxy_list))))
    tasks = []
    for inner in unique:
        if not inner[0]:
            continue
        if str(inner[1]) == '80':
            continue
        tasks.append(Proxy(*inner).test())
    rst = await asyncio.gather(*tasks)
    rst = list(filter(lambda x:x[0]!=float('inf'),rst))
    await client.sadd("proxy", *rst)
    print("channel {} test passed ".format(channel))


async def startup(app):
    def func(channel):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        rst = new_loop.run_until_complete(
            asyncio.ensure_future(grab_and_store(channel)))
        return rst
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(max_workers=7)
    [loop.run_in_executor(executor, func, channel) for channel in CHANS]


app = Application()
app.on_startup.append(startup)
app.router.add_get('/get', get_proxy)
web.run_app(app, host='127.0.0.1', port=7080)
print("app run on http://127.0.0.1:7080")
