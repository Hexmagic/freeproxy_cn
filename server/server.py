from aiohttp import web


async def get_proxy(request):
    return web.json_response({"ac": "bd"})


class Application(web.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)


app = Application()
app.router.add_get('/get', get_proxy)
web.run_app(app, host='127.0.0.1', port=7080)
print("app run on http://127.0.0.1:7080")
