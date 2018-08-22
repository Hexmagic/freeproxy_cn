import unittest
from freeproxy.channels.ipjiang import IPJiang
import asyncio


class Test_ipjiang(unittest.TestCase):
    def test_ipjiang(self):
        coro = IPJiang().batch()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)


def main():
    unittest.main()


if __name__ == '__main__':

    main()