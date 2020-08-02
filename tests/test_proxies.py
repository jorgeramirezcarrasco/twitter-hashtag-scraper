import unittest
from twitter_hashtag_scraper import TwitterHashtagScraper


class TestProxies(unittest.TestCase):


    def setUp(self):
        self.ths = TwitterHashtagScraper(hashtag="test",use_proxy=True)

    def test_get_proxies(self):
        self.assertGreater(len(self.ths._init_proxies()), 0, "List of proxies should be bigger than 0")
        
if __name__ == '__main__':
    unittest.main()
