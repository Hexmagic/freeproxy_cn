import unittest
from freeproxy.channels.sixsix import SixSix
import asyncio


class Test_Sixsix(unittest.TestCase):
    def test_sixsix(self):
        coro = SixSix().batch()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
