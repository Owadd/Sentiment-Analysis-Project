import tweepy

# Replace with your Twitter Bearer Token
bearer_token = "AAAAAAAAAAAAAAAAAAAAALGYtgEAAAAAvfG8cmDlRJ2TCVBgdqyl6qtnbOE%3Dx0k5tCfjSYonrp9TuzUrQT6Nnnkl0oHaxGeNOfcSWNTVwH2oyF"

# Create a StreamingClient object
client = tweepy.StreamingClient(bearer_token)

# Define a class to handle streamed tweets (listener)
class BitcoinStreamListener(tweepy.StreamingClient):

    def on_tweet(self, tweet):
        # Check if the tweet text contains our keywords
        if any(keyword in tweet.text.lower() for keyword in ["bitcoin", "#BTC"]):
            print(f"Tweet Text: {tweet.text}")
            print("-" * 40)

# Initiate the filtered stream using the listener
listener = client.filter.listen(BitcoinStreamListener())  # This line is changed

# This will continue listening for tweets in the background until manually stopped
# You can add logic here to handle stopping the stream (e.g., using a loop with a break condition)

print("Started listening for tweets containing 'bitcoin' or '#BTC'")