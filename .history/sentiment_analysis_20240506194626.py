import tweepy

# Define a subclass of StreamListener to customize tweet handling
class BitcoinStreamListener(tweepy.Stream):
    def on_status(self, status):
        print(status.text)  # Print the text of the tweet
        # You can add further processing or handling of the tweets here

# Replace with your Bearer Token obtained from Twitter developer dashboard (OAuth 2.0 App Only)
bearer_token = "AAAAAAAAAAAAAAAAAAAAAGmvtgEAAAAAR9vjUaPseLjdyQZIag9ilZN%2FyOA%3D8rn5hs0NfkFkHMPMcyVc5jbt0goLBFsNY1I7oMdBYJNRmXsKmQ"

# Authenticate with Twitter API
auth = tweepy.OAuth2BearerHandler(bearer_token)
api = tweepy.API(auth)

# Initialize the streaming client with your credentials and listener
stream_listener = BitcoinStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

# Define the keywords to track
keywords = ["bitcoin", "#BTC"]

# Connect to the streaming API and filter tweets by the defined keywords
stream.filter(track=keywords)
