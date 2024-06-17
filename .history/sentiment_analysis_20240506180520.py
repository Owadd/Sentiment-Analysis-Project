import tweepy

# Define a subclass of StreamingClient to customize tweet handling
class BitcoinStreamListener(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(tweet.text)  # Print the text of the tweet
        # You can add further processing or handling of the tweets here

# Set up your Twitter API credentials
bearer_token = "AAAAAAAAAAAAAAAAAAAAALGYtgEAAAAAjYPPsY7hjMlqWDLAx5uhA1bn5OQ%3D0EQasqFdzxo0HkmuNFEnFzuFeIEvW2Iqc6RzMYkDbqIsVy1qYh"

# Initialize the streaming client with your bearer token
streaming_client = BitcoinStreamListener(bearer_token)

# Define the keywords to track
keywords = ["bitcoin", "#BTC"]

# Connect to the streaming API and filter tweets by the defined keywords
streaming_client.filter(keywords, threaded=True)
