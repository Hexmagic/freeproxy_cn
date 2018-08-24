import json

from aiohttp import web

from freeproxy.config import SERVER_PORT
from freeproxy.util.tools import getRedis

redis = getRedis()


async def get_http_proxy(request):
    one = await redis.srandmember('http_proxy', 1)
    if one:
        try:
            proxy = json.loads(one[0])
        except Exception:
            proxy = eval(one[0])
    return web.json_response(proxy)


async def get_https_proxy(request):
    one = await redis.srandmember('https_proxy', 1)
    if one:
        try:
            proxy = json.loads(one[0])
        except Exception:
            proxy = eval(one[0])
    return web.json_response(proxy)


class Application(web.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)


app = Application()
app.router.add_get('/get_http_proxy', get_http_proxy)
app.router.add_get('/get_https_proxy', get_https_proxy)
web.run_app(app, host='127.0.0.1', port=SERVER_PORT)
print("app run on http://127.0.0.1:{}".format(SERVER_PORT))
