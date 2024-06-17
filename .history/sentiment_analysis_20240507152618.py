import tweepy
import configparser
import pandas as pd

# Read configs
config = configparser.ConfigParser()
config.read('config.ini')

bearer_token = config['twitter']['bearer_token']

# Create a streaming client with rate limiting
client = tweepy.StreamingClient(bearer_token, wait_on_rate_limit=True)

class MyStreamListener(tweepy.StreamListener):
    def __init__(self):
        super().__init__()
        self.tweets = []
        self.limit = 10  # Limit the number of tweets received
        self.tweet_count = 0

    def on_data(self, data):
        if self.tweet_count < self.limit:
            tweet = tweepy.json.loads(data)
            if 'text' in tweet:
                self.tweets.append([tweet['user']['screen_name'], tweet['text']])
            elif 'extended_tweet' in tweet:
                self.tweets.append([tweet['user']['screen_name'], tweet['extended_tweet']['full_text']])
            self.tweet_count += 1
            return True
        else:
            return False

    def on_error(self, status_code):
        print("Error:", status_code)

# Create an instance of the stream listener
my_stream_listener = MyStreamListener()

# Start streaming with rate limiting
client.filter(stream_listener=my_stream_listener, keywords=['2024', '#python'])

# Create DataFrame
columns = ['User', 'Tweet']
df = pd.DataFrame(my_stream_listener.tweets, columns=columns)
print(df)
