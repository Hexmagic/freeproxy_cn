import unittest
from freeproxy_cn.site.crossin import Crossin
from freeproxy_cn.site.eight9 import Eight9
from freeproxy_cn.site.ip3366 import Ip3366
from freeproxy_cn.site.iphai import IPHai
from freeproxy_cn.site.ipjiang import IPJiang
from freeproxy_cn.site.kuai import Kuai
from freeproxy_cn.site.seofang import SeoFang
from freeproxy_cn.site.threeone import ThreeOneF
from freeproxy_cn.site.xiaosu import XiaoSu
from freeproxy_cn.site.xici import XiCi
from freeproxy_cn.site.I337 import I337
from freeproxy_cn.site.super import Super
import asyncio
from freeproxy_cn.core.engine import Engin


class TestChannel(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_threeone(self):
        eng = Engin()
        eng.set_site(ThreeOneF)
        self.loop.run_until_complete(eng.run())

    def test_cross(self):
        eng = Engin()
        eng.set_site(Crossin)
        self.loop.run_until_complete(eng.run())

    def test_eight9(self):
        eng = Engin()
        eng.set_site(Eight9)
        self.loop.run_until_complete(eng.run())

    def test_ip3366(self):
        eng = Engin()
        eng.set_site(Ip3366)
        self.loop.run_until_complete(eng.run())

    def test_iphai(self):
        eng = Engin()
        eng.set_site(IPHai)
        self.loop.run_until_complete(eng.run())

    def test_ipjiang(self):
        eng = Engin()
        eng.set_site(IPJiang)
        self.loop.run_until_complete(eng.run())

    def test_kuai(self):
        eng = Engin()
        eng.set_site(Kuai)
        self.loop.run_until_complete(eng.run())

    def test_seof(self):
        eng = Engin()
        eng.set_site(SeoFang)
        self.loop.run_until_complete(eng.run())

    def test_xiaosu(self):
        eng = Engin()
        eng.set_site(XiaoSu)
        self.loop.run_until_complete(eng.run())

    def test_xici(self):
        eng = Engin()
        eng.set_site(XiCi)
        self.loop.run_until_complete(eng.run())

    def test_super(self):
        eng = Engin()
        eng.set_site(Super)
        self.loop.run_until_complete(eng.run())

    def test_i337(self):
        eng = Engin()
        eng.set_site(I337)
        self.loop.run_until_complete(eng.run())


def main():
    testsuite = unittest.TestSuite()
    testsuite.addTest(TestChannel('test_i337'))
    unittest.TextTestRunner(verbosity=2).run(testsuite)


if __name__ == '__main__':
    main()
