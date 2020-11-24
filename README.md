# Twitter Hashtag Scraper

Unofficial Twitter hashtag scraper using free proxies. No API keys required

---

Installation

```bash
pip install twitter-hashtag-scraper
```

Usage

Import the package and create an object of the scraper using:

- hashtag (str): hashtag to scrap
- x_guest_token (str): a valid token from Twitter. You can check the requests in your browser with Developer Tools, XHR filter and search for a request to https://api.twitter.com/2/search/adaptive.json? to obtain the value from the headers.
- use_proxy (boolean): boolean to activate proxies or not.
- output_path (str, optional): output path. Defaults to None.
- max_tweets (int, optional): max number of tweets to download else try to get tweets until scroll is over. Defaults to None.

Then calling the method collect() will retrieve the data. You need to have a valid x_guest_token checking the requests with Twitter.

```bash
from twitter_hashtag_scraper import TwitterHashtagScraper

TwitterHashtagScraper(hashtag="#MalagaCF",x_guest_token="1331317358300979202",use_proxy=False,output_path="/Users/youruser/Desktop",max_tweets=60).collect()
```
