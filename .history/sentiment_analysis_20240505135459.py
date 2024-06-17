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

# Define a list of Twitter usernames of influencers or analysts in the crypto space
crypto_influencers = ["elonmusk", "VitalikButerin", "cz_binance", ...]  # Replace with relevant usernames

# Function to collect tweets from a list of users
def collect_tweets_from_users(usernames, max_tweets=100, output_file="tweets.json"):
  """
  This function collects tweets from a list of users with a limit on the number of tweets per user.

  Args:
      usernames (list): A list of Twitter usernames to collect tweets from.
      max_tweets (int, optional): The maximum number of tweets to collect per user. Defaults to 100.
      output_file (str, optional): The filename to store the collected tweets in JSON format. Defaults to "tweets.json".

  Returns:
      None
  """

  tweets = []

  for username in usernames:
    try:
      # Get the user object
      user = api.get_user(screen_name=username)

      # Collect tweets from the user's timeline
      new_tweets = list(tweepy.Cursor(api.user_timeline, screen_name=username, count=max_tweets).items(max_tweets))
      tweets.extend(new_tweets)

      # Print progress information
      print(f"Collected {len(new_tweets)} tweets from @{username}")

      # Sleep for a short time to avoid overwhelming Twitter's API
      time.sleep(1)

    except Exception as e:  # Catch any Twitter API errors
      print(f"Error collecting tweets from @{username}: {str(e)}")

  # Save collected tweets to a JSON file
  with open(output_file, 'w') as f:
    json.dump([tweet._json for tweet in tweets], f, indent=4)

  print("Total tweets collected:", len(tweets))
  print("Tweets saved to:", output_file)


# Collect tweets from the list of crypto influencers
collect_tweets_from_users(crypto_influencers, max_tweets=200)