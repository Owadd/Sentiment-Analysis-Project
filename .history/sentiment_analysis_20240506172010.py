import tweepy


consumer_key = 'Wigkff1Ne9GXEtRKSQJ5MopD5'
consumer_secret = 'C6a4uSNEp6HwIGRTFchEn5yQAIElGV4LhBmmew3hjL3qnbFsuu'
access_token = '1668962829368451073-sTzLiyAIGVAxGAn5fVMKHPl80LkLle'
access_token_secret = 'rNPNUcxCxc0mgmR1V8JcrYGocv98SGw8S9nfOUQHglog5'

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Define a class to handle streamed tweets (listener)
class BitcoinStreamListener(tweepy.StreamingClient):

    def on_tweet(self, tweet):
        # Check if the tweet text contains our keywords
        if any(keyword in tweet.text.lower() for keyword in ["bitcoin", "#BTC"]):
            print(f"Tweet Text: {tweet.text}")
            print("-" * 40)

# Create a StreamingClient object
client = tweepy.StreamingClient(auth)

# Define the rules for filtering tweets
rules = tweepy.StreamRule.Rule(value="bitcoin OR #BTC", tag="Bitcoin Stream")

# Create a filter stream object with the defined rules
stream = client.filter.stream(rules=[rules])  # List containing the rule object

# Add the listener to the stream
stream.add_listener(BitcoinStreamListener())

# This code will continue to listen for tweets until manually stopped