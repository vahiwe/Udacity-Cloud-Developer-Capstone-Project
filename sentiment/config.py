from decouple import config

consumer_key = config('TWITTER_CONSUMER_KEY', '')
consumer_secret = config('TWITTER_CONSUMER_SECRET', '')
access_token = config('TWITTER_ACCESS_TOKEN', '')
access_token_secret = config('TWITTER_ACCESS_SECRET', '')