import unittest
from freeproxy.channels import ThreeOneF, Crossin, Eight9, IPHai, Ip3366, IPJiang, Kuai, XiaoSu, XiCi, SeoFang, SixSix, IPhuan
import asyncio


class TestChannel(unittest.TestCase):
    def test_threeone(self):
        coro = ThreeOneF().run()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)

    def test_cross(self):
        coro = Crossin().run()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)

    def test_eight9(self):
        coro = Eight9().run()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)

    def test_ip3366(self):
        coro = Ip3366().run()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)

    def test_iphai(self):
        coro = IPHai().run()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)

    def test_ipjiang(self):
        coro = IPJiang().run()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)

    def test_kuai(self):
        coro = Kuai().run()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)

    def test_seof(self):
        coro = SeoFang().run()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)

    def test_sixsix(self):
        coro = SixSix().run()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)

    def test_xiaosu(self):
        coro = XiaoSu().run()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)

    def test_xici(self):
        coro = XiCi().run()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)

    def test_iphuan(self):
        coro = IPhuan().run()
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.ensure_future(coro))
        print(rst)


def main():
    testsuite = unittest.TestSuite()
    testsuite.addTest(TestChannel('test_threeone'))
    unittest.TextTestRunner(verbosity=2).run(testsuite)


if __name__ == '__main__':
    main()
