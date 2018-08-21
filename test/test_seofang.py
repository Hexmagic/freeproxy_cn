import unittest
from freeproxy.channels.seofang import SeoFang
import asyncio


class Test_seof(unittest.TestCase):
    def test_seof(self):
        coro = SeoFang().batch()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)


def main():
    unittest.main()


if __name__ == '__main__':

    main()