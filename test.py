import requests



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
    ('q', '#MCF'),
    ('count', '20'),
    ('query_source', 'hashtag_click'),
    ('cursor', ''),
    ('pc', '1'),
    ('spelling_corrections', '1'),
    ('ext', 'mediaStats,highlightedLabel'),
)

response = requests.get('https://api.twitter.com/2/search/adaptive.json', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://api.twitter.com/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q=%23MCF&count=20&query_source=hashtag_click&cursor=scroll%3AthGAVUV0VFVBYBFoCs09Sk-aeYIxIYzAESY8LrAAAB9D-AYk3S8an8AAAAFxJxrIQXlhABEgXlF9ZWkAoSWDcN-5dQABIke-nPVrAFEdbw8z5WkAURuGh64leQABJAkzkAFqABEk9pzBZXEAESK-khM9fQBRHrvGzAVgABEbMS6F3X0AASMbSavxeQAQ-XX7DY1-AAEm3UMrrWMAAR4DtVI1YAABJtl9bX1xABEgVsJx6XYAER9YF9gZeABRHi9NCD12ACEm3EWUiXMAASdCSN2FbwARI0C8qVFpAJEeU-QoNU0AMlABUAJQARFciFehWAiXoYB0RFRkFVTFQVABUAFS4VABUAAA%3D%3D&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel', headers=headers)

print(response.content)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://api.twitter.com/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q=%23MCF&count=20&query_source=hashtag_click&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel', headers=headers)
