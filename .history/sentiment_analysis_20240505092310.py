import tweepy
import json

# Replace with your actual API keys
consumer_key = "<YOUR_CONSUMER_KEY>"
consumer_secret = "<YOUR_CONSUMER_SECRET>"
access_token = "<YOUR_ACCESS_TOKEN>"
access_token_secret = "<YOUR_ACCESS_TOKEN_SECRET>"

# Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Define search keywords for Bitcoin
search_query = "Bitcoin OR #Bitcoin OR BTC OR cryptocurrency OR #cryptocurrency OR digital currency"

# Initialize variables for pagination
max_id = None
all_tweets = []

# Collect tweets in batches of 100 (adjust count as needed)
for _ in range(5):  # Adjust the number of loops for desired total count
    tweets = api.search(q=search_query, count=100, max_id=max_id)

    # Update max_id for next iteration (if there are more tweets)
    if len(tweets) > 0:
        max_id = tweets[-1].id_str  # Get the ID of the last tweet

    # Add tweet text to the list
    for tweet in tweets:
        all_tweets.append({"text": tweet.text})

    # Exit loop if no more tweets are available
    if len(tweets) == 0:
        break

# (Optional) Save the collected tweets (text) to a file for further processing
with open("bitcoin_tweets.json", "w") as outfile:
    json.dump(all_tweets, outfile)

print("Collected", len(all_tweets), "tweets.")
