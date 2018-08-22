from aiohttp import web
from freeproxy.util.tools import getRedis
from freeproxy.config import PROXY_KEY, SERVER_PORT
redis = getRedis()
import json


async def get_proxy(request):
    one = await redis.srandmember(PROXY_KEY, 1)
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
app.router.add_get('/get', get_proxy)
web.run_app(app, host='127.0.0.1', port=SERVER_PORT)
print("app run on http://127.0.0.1:{}".format(SERVER_PORT))
