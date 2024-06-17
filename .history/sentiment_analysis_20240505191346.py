import tweepy
import pandas as pd  # Optional, for storing tweets in a DataFrame
import time

# Replace placeholders with your actual Twitter API credentials
consumer_key = "gC44j8IPEE9ipjhgl7CNbhhQd"
consumer_secret = "Qld9VTiICB7ROAGWtq0FIxA63bPDxKBVSo5o4SCJmevaEoA3CT"
access_token = "1668962829368451073-Dbt2nqjfkzOzOeoB2WGv8QHS6ftwRL"   
access_token_secret = "3uugGSLmF5Zc4lavtFqi7Xiv3r9qSEQmyAKvyLRaIOkFx"


# Authenticate to Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define functions for handling tweet data and errors
def on_data(tweet):
    """
    Processes incoming tweets and filters for those containing "Bitcoin" or "BTC".
    Prints relevant information if a matching tweet is found.
    """
    if any(keyword.lower() in tweet.text.lower() for keyword in ["Bitcoin", "BTC"]):
        tweet_text = tweet.text
        created_at = tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")
        print(f"Tweet: {tweet_text}\nCreated at: {created_at}\n")

def on_error(status_code):
    """
    Handles potential errors during stream listening.
    - Rate limiting (status 420): Prints a message, sleeps for 15 minutes, and disconnects.
    - Other errors: Prints the error code.
    """
    if status_code == 420:
        print("Rate limit exceeded! Waiting for 15 minutes...")
        time.sleep(15 * 60)
        return False  # Disconnect stream after rate limit
    else:
        print(f"Error: {status_code}")
    return True  # Keep listening for other errors (potentially with retries)

# Create a stream object and set callback functions
stream = tweepy.StreamListener(auth)
stream.on_data(on_data)
stream.on_error(on_error)

# Filter tweets containing "Bitcoin" or "BTC"
stream.filter(track=["Bitcoin", "BTC"])

# Print instructions to stop the stream manually (Ctrl+C)
print("Press Ctrl+C to stop streaming...")