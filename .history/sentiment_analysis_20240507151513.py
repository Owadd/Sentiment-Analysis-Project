import tweepy
import configparser
import pandas as pd

# read configs
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api=None):
        super(MyStreamListener, self).__init__(api)
        self.tweets = []
        self.limit = 10  # Limit the number of tweets received
        self.tweet_count = 0

    def on_status(self, status):
        if self.tweet_count < self.limit:
            if not status.truncated:
                self.tweets.append([status.user.screen_name, status.text])
            else:
                self.tweets.append([status.user.screen_name, status.extended_tweet['full_text']])
            self.tweet_count += 1
            return True
        else:
            return False

    def on_error(self, status_code):
        print("Error:", status_code)
        if status_code == 420:
            # Returning False in on_error disconnects the stream
            return False

my_stream_listener = MyStreamListener()
my_stream = tweepy.Stream(auth=api.auth, listener=my_stream_listener)
keywords = ['2024', '#python']

# Stream tweets with rate limiting
try:
    my_stream.filter(track=keywords)
except KeyboardInterrupt:
    print("Interrupted")
finally:
    my_stream.disconnect()

# Create DataFrame
columns = ['User', 'Tweet']
df = pd.DataFrame(my_stream_listener.tweets, columns=columns)
print(df)
