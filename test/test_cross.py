import unittest
from freeproxy.channels.crossin import Crossin
import asyncio


class Test_cross(unittest.TestCase):
    def test_cross(self):
        coro = Crossin().batch()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)


def main():
    unittest.main()


if __name__ == '__main__':

    main()