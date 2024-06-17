import tweepy
import pandas as pd
import time

consumer_key = "gC44j8IPEE9ipjhgl7CNbhhQd"
consumer_secret = "Qld9VTiICB7ROAGWtq0FIxA63bPDxKBVSo5o4SCJmevaEoA3CT"
access_token = "1668962829368451073-Dbt2nqjfkzOzOeoB2WGv8QHS6ftwRL"   
access_token_secret = "3uugGSLmF5Zc4lavtFqi7Xiv3r9qSEQmyAKvyLRaIOkFx"


# Authenticate to Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define a function to handle tweet data and errors
def on_data(tweet):
    # Filter for tweets containing "Bitcoin" or "BTC" (case-insensitive)
    if any(keyword.lower() in tweet.text.lower() for keyword in ["Bitcoin", "BTC"]):
        tweet_text = tweet.text
        created_at = tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")
        print(f"Tweet: {tweet_text}\nCreated at: {created_at}\n")

def on_error(status_code):
    if status_code == 420:
        # Handle rate limiting
        print("Rate limit exceeded! Waiting for 15 minutes...")
        time.sleep(15 * 60)
        return False  # Disconnect stream after rate limit
    else:
        print("Error: {}".format(status_code))
    return True  # Keep listening for other errors

# Create a stream object and start listening for tweets
stream = tweepy.Stream(consumer_secret,access_token,access_token_secret)

# Set callback functions for data and errors
stream.on_data(on_data)
stream.on_error(on_error)

# Filter tweets with track keywords
stream.filter(track=["Bitcoin", "BTC"])

# Print instructions to stop the stream manually (Ctrl+C)
print("Press Ctrl+C to stop streaming...")