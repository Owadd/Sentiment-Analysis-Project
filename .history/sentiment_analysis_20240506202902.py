import tweepy

# Define a subclass of StreamingClient to customize tweet handling
class BitcoinStreamListener(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(tweet.text)  # Print the text of the tweet
        # You can add further processing or handling of the tweets here

# Set up your Twitter API credentials
bearer_token = "AAAAAAAAAAAAAAAAAAAAAGmvtgEAAAAAnvolh"+"%"+"2Fp58GwwRlnsfQmUvzIDiQo%3DSVgWmj9S9U1EG6EcVW0Ecp2XZouXq1IZGZoQLOPLJPFdt6BaYt"

# Initialize the streaming client with your bearer token
streaming_client = BitcoinStreamListener(bearer_token)

# Define the keywords to track
keywords = ["bitcoin", "#BTC"]

# Connect to the streaming API and filter tweets by the defined keywords
streaming_client.filter(track=keywords, threaded=True)
