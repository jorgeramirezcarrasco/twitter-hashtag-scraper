import unittest
from scraper.utils import get_proxies


class TestIpRotation(unittest.TestCase):

    def test_get_proxies(self):
        self.assertGreater(len(get_proxies()), 0, "Should be bigger than 0")


if __name__ == '__main__':
    unittest.main()
