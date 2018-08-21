import unittest
from freeproxy.channels.xiaosu import XiaoSu
import asyncio


class Test_xiaosu(unittest.TestCase):
    def test_xiaosu(self):
        coro = XiaoSu().batch()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)


def main():
    unittest.main()


if __name__ == '__main__':

    main()