import tweepy

# Define a subclass of StreamingClient to customize tweet handling
class BitcoinStreamListener(tweepy.StreamingClient):

    def on_tweet(self, tweet):
        print(tweet.text)  # Print the text of the tweet
        # You can add further processing or handling of the tweets here

# Replace with your Bearer Token obtained from Twitter developer dashboard (OAuth 2.0 App Only)
bearer_token = "AAAAAAAAAAAAAAAAAAAAAGmvtgEAAAAAR9vjUaPseLjdyQZIag9ilZN%2FyOA%3D8rn5hs0NfkFkHMPMcyVc5jbt0goLBFsNY1I7oMdBYJNRmXsKmQ"

# Initialize the streaming client with your bearer token
streaming_client = tweepy.StreamingClient(bearer_token=bearer_token)

# Define the keywords to track
keywords = ["bitcoin", "#BTC"]

# Connect to the streaming API and filter tweets by the defined keywords
streaming_client.filter(track=keywords, threaded=True)
