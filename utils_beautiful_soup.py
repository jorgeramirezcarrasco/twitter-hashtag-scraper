from bs4 import BeautifulSoup


def bs_tweet_parser(tweet, tweets_dict, users_dict):
    """Function to parse a tweet with bs

    Arguments:
        tweet {str} -- html code to parse
        tweets_dict {dict} -- dict to store tweets
        users_dict {dict} -- dict to store users

    Returns:
        dict -- dict with tweets stored
        dict -- dict with users stored
    """
    item_tweet = {}
    soup_tweet = BeautifulSoup(str(tweet), "lxml")
    if(soup_tweet.find("span", class_="_timestamp")):
        item_tweet["timestamp"] = soup_tweet.find(
            "span", class_="_timestamp")["data-time"]
    item_tweet["id_tweet"] = soup_tweet.div["data-tweet-id"]
    item_tweet["username"] = soup_tweet.find(
        "a", class_="account-group js-account-group js-action-profile js-user-profile-link js-nav")["href"].replace("/", "@")
    item_tweet["id_user"] = soup_tweet.div["data-user-id"]
    item_tweet["link_tweet"] = "twitter.com" + \
        soup_tweet.div["data-permalink-path"]
    item_tweet["link_user"] = "twitter.com"+soup_tweet.find(
        "a", class_="account-group js-account-group js-action-profile js-user-profile-link js-nav")["href"]
    item_tweet["img_user"] = soup_tweet.find(
        "img", class_="avatar js-action-profile-avatar")["src"]

    item_tweet["text"] = soup_tweet.find(
        "p", class_="TweetTextSize js-tweet-text tweet-text")
    if(item_tweet["text"] is None):
        item_tweet["text"] = soup_tweet.find(
            "p", class_="TweetTextSize js-tweet-text tweet-text tweet-text-rtl").text
    else:
        item_tweet["text"] = soup_tweet.find(
            "p", class_="TweetTextSize js-tweet-text tweet-text").text
    tags_tweet = soup_tweet.find("div", class_="media-tags-container")
    if(tags_tweet):
        tags = tags_tweet.findAll("a", class_="js-user-profile-link")
        for tag in tags:
            if(("data-user-id" in str(tag)) & ("account-group js-user-profile-link" not in str(tag))):
                item_tweet["id_user_tag"] = tag["data-user-id"]
                item_tweet["username_tag"] = tag["href"][1:]
    p_text = soup_tweet.find(
        "p", class_="TweetTextSize js-tweet-text tweet-text")
    if(p_text is None):
        p_text = soup_tweet.find(
            "p", class_="TweetTextSize js-tweet-text tweet-text tweet-text-rtl")
    links_text = p_text.findAll("a")
    for link in links_text:
        if("hashtag_click" in str(link)):
            item_tweet["hashtag"] = link.text[1:]
        if("mentioned" in str(link)):
            item_tweet["id_user_mention"] = link["data-mentioned-user-id"]
            item_tweet["username_mention"] = link.text[1:]
    stats = soup_tweet.find(
        "div", "ProfileTweet-actionCountList u-hiddenVisually")
    counts = stats.findAll("span", class_="ProfileTweet-actionCount")
    item_tweet["replies_count"] = 0
    item_tweet["retweets_count"] = 0
    item_tweet["likes_count"] = 0
    for count in counts:
        if("respuesta" in count.text):
            item_tweet["replies_count"] = count["data-tweet-stat-count"]
        if("retweet" in count.text):
            item_tweet["retweets_count"] = count["data-tweet-stat-count"]
        if("gusta" in count.text):
            item_tweet["likes_count"] = count["data-tweet-stat-count"]

    # Output users
    users_dict["username"].append(
        item_tweet["username"] if item_tweet["username"] else "")
    users_dict["id_user"].append(
        item_tweet["id_user"] if item_tweet["id_user"] else "")
    users_dict["img_user"].append(
        item_tweet["img_user"] if item_tweet["img_user"] else "")
    users_dict["link_user"].append(
        item_tweet["link_user"] if item_tweet["link_user"] else "")

    # Output tweets
    tweets_dict["id_tweet"].append(
        item_tweet["id_tweet"] if item_tweet["id_tweet"] else "")
    tweets_dict["id_user"].append(
        item_tweet["id_user"] if item_tweet["id_user"] else "")
    tweets_dict["user"].append(
        item_tweet["username"] if item_tweet["username"] else "")
    tweets_dict["link_tweet"].append(
        item_tweet["link_tweet"] if item_tweet["link_tweet"] else "")
    tweets_dict["timestamp"].append(
        item_tweet["timestamp"] if item_tweet["timestamp"] else "")
    tweets_dict["text"].append(
        item_tweet["text"] if item_tweet["text"] else "")
    tweets_dict["replies_count"].append(
        item_tweet["replies_count"] if item_tweet["replies_count"] else "")
    tweets_dict["retweets_count"].append(
        item_tweet["retweets_count"] if item_tweet["retweets_count"] else "")
    tweets_dict["likes_count"].append(
        item_tweet["likes_count"] if item_tweet["likes_count"] else "")

    return tweets_dict, users_dict


def bs_retweet_parser(tweet, tweets_dict, users_dict):
    """Function to parse a retweet with bs

    Arguments:
        tweet {str} -- html code to parse
        tweets_dict {dict} -- dict to store tweets
        users_dict {dict} -- dict to store users

    Returns:
        dict -- dict with tweets stored
        dict -- dict with users stored
    """
    item_tweet = {}
    soup_tweet = BeautifulSoup(str(tweet), "lxml")
    if(soup_tweet.find("span", class_="_timestamp")):
        item_tweet["timestamp"] = soup_tweet.find(
            "span", class_="_timestamp")["data-time"]
    elif(soup_tweet.find("span", class_="_timestamp js-short-timestamp js-relative-timestamp")):
        item_tweet["timestamp"] = soup_tweet.find(
            "span", class_="_timestamp js-short-timestamp js-relative-timestamp")["data-time"]

    item_tweet["id_tweet"] = soup_tweet.div["data-tweet-id"]
    item_tweet["username"] = soup_tweet.find(
        "a", class_="account-group js-account-group js-action-profile js-user-profile-link js-nav")["href"].replace("/", "@")
    item_tweet["id_user"] = soup_tweet.div["data-user-id"]
    item_tweet["link_tweet"] = "twitter.com" + \
        soup_tweet.div["data-permalink-path"]
    item_tweet["link_user"] = "twitter.com"+soup_tweet.find(
        "a", class_="account-group js-account-group js-action-profile js-user-profile-link js-nav")["href"]
    item_tweet["img_user"] = soup_tweet.find(
        "img", class_="avatar js-action-profile-avatar")["src"]

    item_tweet["text"] = soup_tweet.find(
        "p", class_="TweetTextSize js-tweet-text tweet-text")
    if(item_tweet["text"] is None):
        item_tweet["text"] = soup_tweet.find(
            "p", class_="TweetTextSize js-tweet-text tweet-text tweet-text-rtl").text
    else:
        item_tweet["text"] = soup_tweet.find(
            "p", class_="TweetTextSize js-tweet-text tweet-text").text
    tags_tweet = soup_tweet.find("div", class_="media-tags-container")
    if(tags_tweet):
        tags = tags_tweet.findAll("a", class_="js-user-profile-link")
        for tag in tags:
            if(("data-user-id" in str(tag)) & ("account-group js-user-profile-link" not in str(tag))):
                item_tweet["id_user_tag"] = tag["data-user-id"]
                item_tweet["username_tag"] = tag["href"][1:]
    p_text = soup_tweet.find(
        "p", class_="TweetTextSize js-tweet-text tweet-text")
    if(p_text is None):
        p_text = soup_tweet.find(
            "p", class_="TweetTextSize js-tweet-text tweet-text tweet-text-rtl")
    links_text = p_text.findAll("a")
    for link in links_text:
        if("hashtag_click" in str(link)):
            item_tweet["hashtag"] = link.text[1:]
        if("mentioned" in str(link)):
            item_tweet["id_user_mention"] = link["data-mentioned-user-id"]
            item_tweet["username_mention"] = link.text[1:]
    stats = soup_tweet.find(
        "div", "ProfileTweet-actionCountList u-hiddenVisually")
    counts = stats.findAll("span", class_="ProfileTweet-actionCount")
    item_tweet["replies_count"] = 0
    item_tweet["retweets_count"] = 0
    item_tweet["likes_count"] = 0
    for count in counts:
        if("respuesta" in count.text):
            item_tweet["replies_count"] = count["data-tweet-stat-count"]
        if("retweet" in count.text):
            item_tweet["retweets_count"] = count["data-tweet-stat-count"]
        if("gusta" in count.text):
            item_tweet["likes_count"] = count["data-tweet-stat-count"]

    # Output users
    users_dict["username"].append(
        item_tweet["username"] if item_tweet["username"] else "")
    users_dict["id_user"].append(
        item_tweet["id_user"] if item_tweet["id_user"] else "")
    users_dict["img_user"].append(
        item_tweet["img_user"] if item_tweet["img_user"] else "")
    users_dict["link_user"].append(
        item_tweet["link_user"] if item_tweet["link_user"] else "")

    # Output tweets
    tweets_dict["id_tweet"].append(
        item_tweet["id_tweet"] if item_tweet["id_tweet"] else "")
    tweets_dict["id_user"].append(
        item_tweet["id_user"] if item_tweet["id_user"] else "")
    tweets_dict["user"].append(
        item_tweet["username"] if item_tweet["username"] else "")
    tweets_dict["link_tweet"].append(
        item_tweet["link_tweet"] if item_tweet["link_tweet"] else "")
    tweets_dict["timestamp"].append(
        item_tweet["timestamp"] if item_tweet["timestamp"] else "")
    tweets_dict["text"].append(
        item_tweet["text"] if item_tweet["text"] else "")
    tweets_dict["replies_count"].append(
        item_tweet["replies_count"] if item_tweet["replies_count"] else "")
    tweets_dict["retweets_count"].append(
        item_tweet["retweets_count"] if item_tweet["retweets_count"] else "")
    tweets_dict["likes_count"].append(
        item_tweet["likes_count"] if item_tweet["likes_count"] else "")

    return tweets_dict, users_dict


def bs_twitter_tweets_retweets_extractor_iterator(data_from_request):
    """Function to parse a Twitter html

    Arguments:
        tweedata_from_requestt {str} -- html code to parse
        tweets_dict {dict} -- [dict to store tweets
        users_dict {dict} -- [dict to store users

    Returns:
        dict -- dict with tweets to parse
        dict -- dict with retweets to parse

    """

    soup = BeautifulSoup(data_from_request["items_html"], "lxml")
    retweets = soup.findAll(
        "div", class_="tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content original-tweet js-original-tweet tweet-has-context ")
    retweetscards = soup.findAll(
        "div", class_="tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content original-tweet js-original-tweet tweet-has-context has-cards has-content ")
    retweets = retweets+retweetscards
    tweets = soup.findAll("div", class_="original-tweet")
    tweetscards = soup.findAll(
        "div", class_="tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content original-tweet js-original-tweet has-cards cards-forward ")
    tweets = tweets + tweetscards
    return tweets, retweets
