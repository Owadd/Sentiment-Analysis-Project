import tweepy
import json

# Define Twitter API credentials 
consumer_key = "gC44j8IPEE9ipjhgl7CNbhhQd"
consumer_secret = "Qld9VTiICB7ROAGWtq0FIxA63bPDxKBVSo5o4SCJmevaEoA3CT"
access_token = "1668962829368451073-Dbt2nqjfkzOzOeoB2WGv8QHS6ftwRL"
access_token_secret = "3uugGSLmF5Zc4lavtFqi7Xiv3r9qSEQmyAKvyLRaIOkFx"

# Function to handle the streaming connection and process tweets
def listen_to_stream(keywords):
  # Authentication object with generated tokens
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)

  # Create stream object and connect to Streaming API
  stream = tweepy.Stream(auth=auth)


  # Start listening for tweets containing the keywords
  try:
    stream.filter(track=keywords)
  except tweepy.TweepyError as e:
    print(f"Error streaming tweets: {e}")
    # Handle errors gracefully (e.g., retry logic, exit program)

# Define keywords to track (replace with your desired keywords/hashtags)
keywords = ["#MachineLearning", "#ArtificialIntelligence", "#Python"]

# Start listening for tweets
listen_to_stream(keywords)