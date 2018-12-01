from freeproxy.site import SITES
import asyncio
from freeproxy.core.engine import Engin
eng = Engin()
eng.load_sites(SITES)
loop = asyncio.get_event_loop()
loop.run_until_complete(eng.run())