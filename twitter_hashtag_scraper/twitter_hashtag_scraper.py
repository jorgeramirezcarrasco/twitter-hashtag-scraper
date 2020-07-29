# TwitterHashtagScraper
# Copyright 2020 Jorge Ramírez Carrasco
# See LICENSE for details.

import csv
import json
import math
import sys
import time
from datetime import datetime
from itertools import cycle
from re import findall

import requests

import pandas as pd
from bs4 import BeautifulSoup
from .utils_beautiful_soup import (
    bs_retweet_parser, bs_tweet_parser,
    bs_twitter_tweets_retweets_extractor_iterator)


class TwitterHashtagScraper():
    """Twitter Hashtag Scraper
    """

    def __init__(self, hashtag, use_proxy, output_path=None, max_tweets=None):
        """Twitter Hashtag Scraper constructor

        Args:
            hashtag (str): hashtag to scrap
            use_proxy (boolean): boolean to activate proxies or not
            output_path (str, optional): output path. Defaults to None.
            max_tweets (int, optional): max number of tweets to download else try to get tweets until scroll is over. Defaults to None.
        """
        
        self.hashtag = hashtag
        self.use_proxy = use_proxy
        self.output_path = output_path
        self.max_tweets = max_tweets

    def _init_proxies(self):
        """Function to obtain available proxies from sslproxies

        Returns:
            [list] -- list of proxies
        """
        r = requests.get('https://www.sslproxies.org/')
        matches = findall(r"<td>\d+.\d+.\d+.\d+</td><td>\d+</td>", r.text)
        revised = [m.replace('<td>', '') for m in matches]
        proxies = [s[:-5].replace('</td>', ':') for s in revised]
        return proxies

    def _make_request(self, proxy_active, proxy_active_value, url, headers, params):
        """Function to make a request through a proxy

        Arguments:
            proxy_active {int} -- boolean about the active proxy
            proxy_active_value {str} -- active proxy
            url {str} -- url to make the request
            headers {dict} -- headers to send with the request
            params {dict} -- params to send with the request

        Returns:
            [int, str, dict] -- proxy information and result of the request
        """
        if self.use_proxy:
            proxies = self._init_proxies()
            proxy_pool = cycle(proxies)
            # Iterate trying free proxies to make the request
            for i in range(100):
                if proxy_active != 1:
                    proxy_active_value = next(proxy_pool)
                try:
                    response = requests.get('https://httpbin.org/ip', timeout=3.0, proxies={
                                            "http": 'http://' + proxy_active_value, "https": 'https://' + proxy_active_value})
                    page = requests.get(url, headers=headers, params=params, proxies={
                                        "http": 'http://' + proxy_active_value, "https": 'https://' + proxy_active_value})
                    proxy_active = 1
                    if page.status_code == 200:
                        return proxy_active, proxy_active_value, page
                except Exception as e:
                    proxy_active = 0
                    continue
            return proxy_active, proxy_active_value, "Error"
        else:
            page = requests.get(url, headers=headers, params=params)
            proxy_active = 0
            if page.status_code == 200:
                return proxy_active, None, page




    def _get_hashtag_timeline(self):
        """Function to obain the hashtag timeline from Twitter

        Returns:
            dict -- dict with tweets stored
            dict -- dict with users stored
        """
        tweets_dict = self._create_dict_from_structure('tweets_hashtag')
        users_dict = self._create_dict_from_structure('users_hashtag')

        print(f"Collecting data from Twitter about: {self.hashtag}")

        has_more_items = True
        last_tweet_id = 0
        count_tweets = 0
        proxy_active = 0
        proxy_active_value = ""
        min_position = math.inf
        try:
            # Iterate simulating scroll
            while (has_more_items):
                print(f"{count_tweets}/{self.max_tweets if self.max_tweets else 'Max Scroll'} tweets obtained...")
                headers = {
                    'Host': 'twitter.com',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Referer': 'https://twitter.com/hashtag/'+str(self.hashtag)+'?f=tweets&vertical=default&src=hash',
                    'X-Twitter-Active-User': 'yes',
                    'X-Requested-With': 'XMLHttpRequest',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                }

                params = (
                    ('f', 'tweets'),
                    ('vertical', 'default'),
                    ('q', '#'+str(self.hashtag)+''),
                    ('src', 'hash'),
                    ('lang', 'es'),
                    ('max_position', str(min_position)),
                    ('reset_error_state', 'false'),
                )

                url = 'https://twitter.com/i/search/timeline'
                proxy_active, proxy_active_value, page = self._make_request(
                    proxy_active, proxy_active_value, url, headers, params)

                data = json.loads(page.content)
                min_position = data["min_position"]
                (tweets, retweets) = bs_twitter_tweets_retweets_extractor_iterator(data)
                for tweet in tweets:
                    (tweets_dict, users_dict) = bs_tweet_parser(
                        tweet, tweets_dict, users_dict)
                for tweet in retweets:
                    (tweets_dict, users_dict) = bs_retweet_parser(
                        tweet, tweets_dict, users_dict)

                count_tweets = count_tweets+20
                if len(tweets_dict["id_tweet"]) > 0:
                    if last_tweet_id == tweets_dict["id_tweet"][-1]:
                        has_more_items = False
                    last_tweet_id = tweets_dict["id_tweet"][-1]
                else:
                    has_more_items = False

                if self.max_tweets:
                    if count_tweets > self.max_tweets:
                        has_more_items = False

                time.sleep(0.1)
        except Exception as e:
            print(e)

        return tweets_dict, users_dict

    def _create_dict_from_structure(self, key):
        """Function to create a dict structure from the template defined in the json

        Arguments:
            key {str} -- key in the json artifact

        Returns:
            dict -- template dict to fill
        """
        
        json_file_item = {"tweets_hashtag": [
                                "id_tweet",
                                "id_user",
                                "user",
                                "link_tweet",
                                "timestamp",
                                "text",
                                "replies_count",
                                "retweets_count",
                                "likes_count"
                            ],
                            "users_hashtag": [
                                "username",
                                "id_user",
                                "img_user",
                                "link_user"
                            ]
                        }
        dict_struct = {}
        for column in json_file_item[key]:
            dict_struct[column] = []
        return dict_struct

    def collect(self):
        """Function to execute a search on twitter from the initial term
        """
    
        tweets_dict, users_dict = self._get_hashtag_timeline()

        tweets_df = pd.DataFrame(tweets_dict)
        users_df = pd.DataFrame(users_dict).drop_duplicates()

        date_str = str(datetime.now()).split(' ')[0]
        if self.output_path:
            tweets_df.to_csv(f'{self.output_path}/results_{self.hashtag}_{date_str}.csv', index=False)
            users_df.to_csv(f'{self.output_path}/results_users_{self.hashtag}_{date_str}.csv', index=False)
        else:
            tweets_df.to_csv(f'./results_{self.hashtag}_{date_str}.csv', index=False)
            users_df.to_csv(f'./results_users_{self.hashtag}_{date_str}.csv', index=False)
