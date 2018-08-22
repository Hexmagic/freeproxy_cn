import unittest
from freeproxy.channels.iphai import IPHai
import asyncio


class Test_iphai(unittest.TestCase):
    def test_iphai(self):
        coro = IPHai().batch()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)


def main():
    unittest.main()


if __name__ == '__main__':

    main()