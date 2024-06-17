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


# Function to collect tweets for a given query
def collect_tweets(query, max_tweets=100, output_file="tweets.json"):
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
  max_id = None

  while len(tweets) < max_tweets:
    try:
      if max_id:
        # If we already have some tweets, use max_id to get older tweets
        new_tweets = api.search_tweets(q=query, count=100, max_id=max_id)
      else:
        # For the first iteration, get the most recent tweets
        new_tweets = list(tweepy.Cursor(api.search, q=query, count=100).items(100))  # Fetch the first 100 tweets

      # Check if no more tweets found for the query
      if not new_tweets:
        print("No more tweets found for query:", query)
        break

      # Extend the tweets list with the new tweets
      tweets.extend(new_tweets)

      # Update max_id for the next iteration to get older tweets
      max_id = new_tweets[-1].id - 1

      # Print progress information
      print("Collected {} tweets so far.".format(len(tweets)))

      # Sleep for a short time to avoid overwhelming Twitter's API
      time.sleep(1)

    except Exception as e:  # Catch any Twitter API errors
      print("Error:", str(e))
      break  # Exit the loop on error

  # Save collected tweets to a JSON file
  with open(output_file, 'w') as f:
    json.dump([tweet._json for tweet in tweets], f, indent=4)

  print("Total tweets collected:", len(tweets))
  print("Tweets saved to:", output_file)


# Function to collect tweets in batches for larger datasets
def collect_tweets_in_batches(query, total_tweets, batch_size=1000):
  """
  This function collects a large number of tweets in batches to manage memory and avoid overwhelming Twitter's API.

  Args:
      query (str): The search query to use for collecting tweets.
      total_tweets (int): The total number of tweets to collect.
      batch_size (int, optional): The number of tweets to collect in each batch. Defaults to 1000.

  Returns:
      None
  """

  # Calculate the number of batches required
  num_batches = total_tweets // batch_size

  for i in range(num_batches):
    # Print information about the current batch
    print("Batch", i+1, "of", num_batches)

    # Define the output filename for the current batch
    output_file = f"tweets_batch_{i+1}.json"

    # Call the collect_tweets function for each batch
    collect_tweets(query, max_tweets=batch_size, output_file=output_file)

    # Sleep for a longer time between batches to be more respectful of Twitter's API limits
    time.sleep(60)  # Sleep for 1 minute


# Example usage
query = "bitcoin"
total_tweets_to_collect = 5000
collect_tweets_in_batches(query, total_tweets_to_collect)
