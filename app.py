from freeproxy_cn import Engin
import asyncio
loop = asyncio.get_event_loop()
loop.run_until_complete(Engin().run())
