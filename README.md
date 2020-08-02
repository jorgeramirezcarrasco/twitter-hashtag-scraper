# Twitter Hashtag Scraper

Unofficial Twitter hashtag scraper using free proxies. No API keys required

----

Installation

```bash
pip install twitter-hashtag-scraper 
```

Usage

Import the package and create an object of the scraper using:
* hashtag (str): hashtag to scrap
* use_proxy (boolean): boolean to activate proxies or not
* output_path (str, optional): output path. Defaults to None.
* max_tweets (int, optional): max number of tweets to download else try to get tweets until scroll is over. Defaults to None.


Then calling the method collect() will retrieve the data

```bash 
from twitter_hashtag_scraper import TwitterHashtagScraper

TwitterHashtagScraper(hashtag="#MalagaCF",use_proxy=True,output_path="/Users/myuser/Desktop",max_tweets=None).collect()

```


