# Import libraries
import tweepy
import json
from textblob import TextBlob

# Define Twitter API credentials 
consumer_key = "gC44j8IPEE9ipjhgl7CNbhhQd"
consumer_secret = "Qld9VTiICB7ROAGWtq0FIxA63bPDxKBVSo5o4SCJmevaEoA3CT"
access_token = "1668962829368451073-Dbt2nqjfkzOzOeoB2WGv8QHS6ftwRL"
access_token_secret = "3uugGSLmF5Zc4lavtFqi7Xiv3r9qSEQmyAKvyLRaIOkFx"

# Class to handle incoming tweets from the stream
class MyStreamListener(tweepy.StreamListener):

  def on_status(self, status):
    # Extract tweet information (text, timestamp, etc.)
    tweet_text = status.text
    created_at = status.created_at

    # Perform sentiment analysis using TextBlob
    sentiment = TextBlob(tweet_text).sentiment
    polarity = sentiment.polarity  # Positive: > 0, Negative: < 0, Neutral: 0

    # Store tweet data with sentiment analysis in a dictionary
    tweet_data = {
        "text": tweet_text,
        "created_at": created_at.isoformat(),  # Convert timestamp to ISO format
        "polarity": polarity
    }

    # Append tweet data to a list (can be replaced with database storage)
    with open("tweets.json", "a") as f:
      json.dump(tweet_data, f, indent=4)

    print(f"Received tweet: {tweet_text} - Sentiment: {polarity}")
    return True  # Keep listening for more tweets

# Create authentication object with generated tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create stream object and connect to Streaming API
stream = tweepy.Stream(auth, MyStreamListener())

# Define keywords to track in the stream (replace with your crypto keywords)
keywords = ["bitcoin", "#BTC", "ethereum", "#ETH"]

# Start listening for tweets containing the keywords
stream.filter(track=keywords)
