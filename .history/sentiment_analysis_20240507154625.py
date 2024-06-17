import tweepy
import configparser
import pandas as pd

# Read configs
config = configparser.ConfigParser()
config.read('config.ini')

bearer_token = config['twitter']['bearer_token']

# Create a streaming client with rate limiting
client = tweepy.StreamingClient(bearer_token)

# Define keywords to filter tweets
keywords = ['2024', '#python']

# Add rules for filtering
client.add_rules([tweepy.StreamRule(value=keyword) for keyword in keywords])

# Create an empty list to store tweets
tweets = []

# Define a function to handle incoming tweets
def on_tweet(tweet):
    global tweets
    if len(tweets) < 10:  # Limit the number of tweets received
        if 'text' in tweet:
            tweets.append([tweet['user']['screen_name'], tweet['text']])
        elif 'extended_tweet' in tweet:
            tweets.append([tweet['user']['screen_name'], tweet['extended_tweet']['full_text']])
        return True
    else:
        return False

# Start streaming with rate limiting
client.filter(on_tweet=on_tweet)

# Create DataFrame
columns = ['User', 'Tweet']
df = pd.DataFrame(tweets, columns=columns)
print(df)
