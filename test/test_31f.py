import unittest
from freeproxy.channels.threeone import  ThreeOneF
import asyncio


class Test_threeone(unittest.TestCase):
    def test_threeone(self):
        coro = ThreeOneF().batch()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)


def main():
    unittest.main()


if __name__ == '__main__':

    main()