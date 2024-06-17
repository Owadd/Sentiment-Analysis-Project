# Import libraries
import tweepy
import json


# Define Twitter API credentials 
consumer_key = "gC44j8IPEE9ipjhgl7CNbhhQd"
consumer_secret = "Qld9VTiICB7ROAGWtq0FIxA63bPDxKBVSo5o4SCJmevaEoA3CT"
access_token = "1668962829368451073-Dbt2nqjfkzOzOeoB2WGv8QHS6ftwRL"
access_token_secret = "3uugGSLmF5Zc4lavtFqi7Xiv3r9qSEQmyAKvyLRaIOkFx"


# Create authentication object with generated tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Define keywords to track in the stream (replace with your crypto keywords)
keywords = ["bitcoin", "#BTC"]

# Function to handle the streaming connection and process tweets
def on_status(status):
    # Extract tweet information (text, timestamp, etc.)
    tweet_text = status.text
    created_at = status.created_at

    # Perform sentiment analysis or store the tweet data (logic here)
    # ... (your sentiment analysis or data storage code) ...

    print(f"Received tweet: {tweet_text} - Created at: {created_at}")

# Function to handle the streaming connection and process tweets
def listen_to_stream(keywords):
    # Create stream object and connect to Streaming API
    stream = tweepy.Stream(auth=auth, listener=on_status)

    # Start listening for tweets containing the keywords
    stream.filter(track=keywords)

# Start listening for tweets
listen_to_stream(keywords)