import unittest
from freeproxy.channels import ThreeOneF, Crossin, Eight9, IPHai, Ip3366, IPJiang, Kuai, XiaoSu, XiCi, SeoFang, SixSix
import asyncio


class TestChannel(unittest.TestCase):
    def test_threeone(self):
        coro = ThreeOneF().batch()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)

    def test_cross(self):
        coro = Crossin().batch()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)

    def test_eight9(self):
        coro = Eight9().batch()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)

    def test_ip3366(self):
        coro = Ip3366().batch()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)

    def test_iphai(self):
        coro = IPHai().batch()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)

    def test_ipjiang(self):
        coro = IPJiang().batch()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)

    def test_kuai(self):
        coro = Kuai().batch()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)

    def test_seof(self):
        coro = SeoFang().batch()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)

    def test_sixsix(self):
        coro = SixSix().batch()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)

    def test_xiaosu(self):
        coro = XiaoSu().batch()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)

    def test_xici(self):
        coro = XiCi().batch()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)


def main():
    unittest.main()


if __name__ == '__main__':

    main()
