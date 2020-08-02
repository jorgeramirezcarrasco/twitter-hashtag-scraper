import unittest
import math
from twitter_hashtag_scraper import TwitterHashtagScraper


class TestRequests(unittest.TestCase):


    def setUp(self):
        self.ths = TwitterHashtagScraper(hashtag="test",use_proxy=False)

    def test_make_request(self):
        min_position = math.inf
        headers = {
                    'Host': 'twitter.com',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Referer': 'https://twitter.com/hashtag/'+str(self.ths.hashtag)+'?f=tweets&vertical=default&src=hash',
                    'X-Twitter-Active-User': 'yes',
                    'X-Requested-With': 'XMLHttpRequest',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                }

        params = (
            ('f', 'tweets'),
            ('vertical', 'default'),
            ('q', '#'+str(self.ths.hashtag)+''),
            ('src', 'hash'),
            ('lang', 'es'),
            ('max_position', str(min_position)),
            ('reset_error_state', 'false'),
        )

        url = 'https://twitter.com/i/search/timeline'
        proxy_active, proxy_active_value, page = self.ths._make_request(0, "", url, headers, params)
        self.assertTrue(page.status_code == 200, "Request not using proxy replying status code != 200")
        
if __name__ == '__main__':
    unittest.main()
