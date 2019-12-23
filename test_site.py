import unittest
from freeproxy_cn.site import SITES
import asyncio
from tqdm import tqdm


class TestChannel(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_sites(self):
        for site in tqdm(SITES, desc='test process'):
            site_instance = site()
            rst = site_instance.run()
            print(rst)

    def test_site(self):
        site = SITES[8]
        site = site(debug=True)
        loop = asyncio.get_event_loop()
        rst = loop.run_until_complete(asyncio.gather(site.run()))
        print(rst)


def main():
    testsuite = unittest.TestSuite()
    testsuite.addTest(TestChannel('test_site'))
    unittest.TextTestRunner(verbosity=2).run(testsuite)


if __name__ == '__main__':
    main()
