import tweepy
import json
import time

# Define Twitter API credentials (replace with your actual keys)
consumer_key = 'gC44j8IPEE9ipjhgl7CNbhhQd'
consumer_secret = 'Qld9VTiICB7ROAGWtq0FIxA63bPDxKBVSo5o4SCJmevaEoA3CT'
access_token = '1668962829368451073-Dbt2nqjfkzOzOeoB2WGv8QHS6ftwRL'
access_token_secret = '3uugGSLmF5Zc4lavtFqi7Xiv3r9qSEQmyAKvyLRaIOkFx'

# Authenticate to Twitter API
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Function to collect tweets using search (deprecated endpoint)
def collect_tweets_by_search(query, max_tweets=100, output_file="tweets.json"):
  """
  This function collects tweets for a given search query with a limit on the number of tweets.

  Args:
      query (str): The search query to use for collecting tweets.
      max_tweets (int, optional): The maximum number of tweets to collect. Defaults to 100.
      output_file (str, optional): The filename to store the collected tweets in JSON format. Defaults to "tweets.json".

  Returns:
      None
  """

  tweets = []

  try:
    # Use search/tweets with lower rate limits and potentially less data
    new_tweets = list(tweepy.