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
from utils_json import json_tweet_parser


class TwitterHashtagScraper():
    """Twitter Hashtag Scraper
    """

    def __init__(self, hashtag, x_guest_token, use_proxy, output_path=None, max_tweets=None):
        """Twitter Hashtag Scraper constructor

        Args:
            hashtag (str): hashtag to scrap
            x_guest_token (str): a valid guest token
            use_proxy (boolean): boolean to activate proxies or not
            output_path (str, optional): output path. Defaults to None.
            max_tweets (int, optional): max number of tweets to download else try to get tweets until scroll is over. Defaults to None.
        """
        
        self.hashtag = hashtag
        self.use_proxy = use_proxy
        self.output_path = output_path
        self.max_tweets = max_tweets
        self.x_guest_token = x_guest_token

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
                    response = requests.get('https://httpbin.org/ip', timeout=2.0, proxies={
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
                        'authority': 'api.twitter.com',
                        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                        'x-twitter-client-language': 'es',
                        'x-guest-token': str(self.x_guest_token),
                        'x-twitter-active-user': 'yes',
                        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
                        'accept': '*/*',
                        'origin': 'https://twitter.com',
                        'sec-fetch-site': 'same-site',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-dest': 'empty',
                        'referer': 'https://twitter.com/',
                        'accept-language': 'es-ES,es;q=0.9',
                    }

                params = (
                        ('include_profile_interstitial_type', '1'),
                        ('include_blocking', '1'),
                        ('include_blocked_by', '1'),
                        ('include_followed_by', '1'),
                        ('include_want_retweets', '1'),
                        ('include_mute_edge', '1'),
                        ('include_can_dm', '1'),
                        ('include_can_media_tag', '1'),
                        ('skip_status', '1'),
                        ('cards_platform', 'Web-12'),
                        ('include_cards', '1'),
                        ('include_ext_alt_text', 'true'),
                        ('include_quote_count', 'true'),
                        ('include_reply_count', '1'),
                        ('tweet_mode', 'extended'),
                        ('include_entities', 'true'),
                        ('include_user_entities', 'true'),
                        ('include_ext_media_color', 'true'),
                        ('include_ext_media_availability', 'true'),
                        ('send_error_codes', 'true'),
                        ('simple_quoted_tweet', 'true'),
                        ('q', '#'+str(self.hashtag)+''),
                        ('count', '20'),
                        ('query_source', 'hashtag_click'),
                        ('cursor', str(min_position)),
                        ('pc', '1'),
                        ('spelling_corrections', '1'),
                        ('ext', 'mediaStats,highlightedLabel'),
                    )


                url = 'https://api.twitter.com/2/search/adaptive.json'
                proxy_active, proxy_active_value, page = self._make_request(
                    proxy_active, proxy_active_value, url, headers, params)
                data = json.loads(page.content)
                cursor_item_init = [d for d in data["timeline"]["instructions"][0]["addEntries"]["entries"] if d['entryId'] == 'sq-cursor-bottom']
                if cursor_item_init:
                    cursor_item = cursor_item_init[0]
                else:
                    cursor_item = data["timeline"]["instructions"][-1]["replaceEntry"]["entry"]
                min_position = cursor_item["content"]["operation"]["cursor"]["value"]
                for tweet in data["globalObjects"]["tweets"].keys():
                    (tweets_dict, users_dict) = json_tweet_parser(data["globalObjects"]["tweets"][tweet],data["globalObjects"]["users"], tweets_dict, users_dict)
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
