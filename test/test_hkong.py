import unittest
from freeproxy_cn.site2.freecz import freeproxy_cnCz
from freeproxy_cn.site2.nova import Nova
from freeproxy_cn.site2.cool import Cool
from freeproxy_cn.site2.proxydocker import ProxyDocker
from freeproxy_cn.site2.xroxy import Xroxy
from freeproxy_cn.core.engine import Engin
import asyncio


class Testsite2(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_freeproxy_cncz(self):
        eng = Engin()
        eng.set_site(freeproxy_cnCz)
        self.loop.run_until_complete(eng.run())

    def test_nova(self):
        eng = Engin()
        eng.set_site(Nova)
        self.loop.run_until_complete(eng.run())

    def test_proxydocker(self):
        eng = Engin()
        eng.set_site(ProxyDocker)
        self.loop.run_until_complete(eng.run())

    def test_cool(self):
        eng = Engin()
        eng.set_site(Cool)
        self.loop.run_until_complete(eng.run())

    def test_xroxy(self):
        eng = Engin()
        eng.set_site(Xroxy)
        self.loop.run_until_complete(eng.run())


def main():
    testsuite = unittest.TestSuite()
    testsuite.addTest(Testsite2('test_xroxy'))
    unittest.TextTestRunner(verbosity=2).run(testsuite)


if __name__ == '__main__':
    main()
