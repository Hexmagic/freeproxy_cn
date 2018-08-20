import unittest
from freeproxy.channels.eight9 import Eight9
import asyncio


class Test_eight9(unittest.TestCase):
    def test_eight9(self):
        coro = Eight9().batch()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)


def main():
    unittest.main()


if __name__ == '__main__':

    main()