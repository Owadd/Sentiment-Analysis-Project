import tweepy

# Replace with your Twitter Bearer Token
bearer_token = ""

# Create a StreamingClient object
client = tweepy.StreamingClient(bearer_token)

# Define a class to handle streamed tweets (listener)
class BitcoinStreamListener(tweepy.StreamingClient):

    def on_tweet(self, tweet):
        # Check if the tweet text contains our keywords
        if any(keyword in tweet.text.lower() for keyword in ["bitcoin", "#BTC"]):
            print(f"Tweet Text: {tweet.text}")
            print("-" * 40)

# Define the rules for filtering tweets
rules = tweepy.rules.Rule(value="bitcoin OR #BTC", tag="Bitcoin Stream")

# Add the filtering rule to the stream
client.add_rules(rules=[rules])

# Create a filter stream object with the defined rules
stream = client.filter.stream(threaded=True)  # Run stream in a separate thread

# Add the listener to the stream
stream.add_listener(BitcoinStreamListener())

# This will continue listening for tweets in the background until manually stopped
# You can add logic here to handle stopping the stream (e.g., using a loop with a break condition)

print("Started listening for tweets containing 'bitcoin' or '#BTC'")
