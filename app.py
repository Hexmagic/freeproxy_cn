from freeproxy_cn import Engin
import asyncio

loop = asyncio.get_event_loop()
loop.run_until_complete(
    Engin(redis_host="127.0.0.1", redis_port=6379, redis_db=0, redis_password="").run()
)
