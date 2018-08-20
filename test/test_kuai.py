import unittest
from freeproxy.channels.kuai import Kuai
import asyncio


class Test_kuai(unittest.TestCase):
    def Test_kuai(self):
        coro = Kuai().batch()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)


def main():
    unittest.main()


if __name__ == '__main__':

    main()