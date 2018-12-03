import unittest
from freeproxy.site.crossin import Crossin
from freeproxy.site.eight9 import Eight9
from freeproxy.site.ip3366 import Ip3366
from freeproxy.site.iphai import IPHai
from freeproxy.site.ipjiang import IPJiang
from freeproxy.site.kuai import Kuai
from freeproxy.site.seofang import SeoFang
from freeproxy.site.threeone import ThreeOneF
from freeproxy.site.xiaosu import XiaoSu
from freeproxy.site.xici import XiCi
from freeproxy.site.zdaye import Zdaye
import asyncio
from freeproxy.core.engine import Engin


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

    def test_zdaye(self):
        eng = Engin()
        eng.set_site(Zdaye)
        self.loop.run_until_complete(eng.run())


def main():
    testsuite = unittest.TestSuite()
    testsuite.addTest(TestChannel('test_zdaye'))
    unittest.TextTestRunner(verbosity=2).run(testsuite)


if __name__ == '__main__':
    main()
