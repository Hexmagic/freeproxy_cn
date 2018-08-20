import unittest
from freeproxy.channels.ip3366 import Ip3366
import asyncio


class Test_ip3366(unittest.TestCase):
    def test_ip3366(self):
        coro = Ip3366().batch()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)


def main():
    unittest.main()


if __name__ == '__main__':

    main()