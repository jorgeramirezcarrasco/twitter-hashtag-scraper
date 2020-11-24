import json

def json_tweet_parser(tweet, users, tweets_dict, users_dict):
    """Function to parse a tweet with bs

    Arguments:
        tweet {str} -- tweet result
        users {dict} -- dict with results
        tweets_dict {dict} -- dict to store tweets
        users_dict {dict} -- dict to store users

    Returns:
        dict -- dict with tweets stored
        dict -- dict with users stored
    """
    item_tweet = {}
    item_tweet["timestamp"] = tweet["created_at"]
    item_tweet["id_tweet"] = tweet["id_str"]
    item_tweet["username"] = users[tweet["user_id_str"]]["screen_name"]
    item_tweet["id_user"] = tweet["user_id_str"]
    item_tweet["link_tweet"] = "twitter.com/"+users[tweet["user_id_str"]]["screen_name"]+"/status/"+tweet["id_str"]
    item_tweet["link_user"] = "twitter.com/"+users[tweet["user_id_str"]]["screen_name"]
    item_tweet["img_user"] = users[tweet["user_id_str"]]["profile_background_image_url_https"]
    item_tweet["text"] = tweet["full_text"]
    item_tweet["replies_count"] = tweet["reply_count"]
    item_tweet["retweets_count"] = tweet["retweet_count"]
    item_tweet["likes_count"] = tweet["favorite_count"]
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
