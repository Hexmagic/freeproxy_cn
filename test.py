import aiohttp
import asyncio
from freeproxy.channels.eight9 import Eight9

class Test(object):
    async def test(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                text = await res.text()
        return text


async def plan():
    tasks = []
    for x in range(5):
        coro = Eight9().batch()
        tasks.append(asyncio.ensure_future(coro))
    rst = await asyncio.gather(*tasks)
    print(rst)


def main():
    coro = plan()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(coro))


if __name__ == '__main__':
    main()
