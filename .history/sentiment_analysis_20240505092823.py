import tweepy
import json
import time

# Replace with your actual API keys
consumer_key = "<loTAvylLh5VUPMsk4Tk3Lmcp3"
consumer_secret = "iojjP3yQRf3JKLgtJ75N8Cj25SYuyl0ybDRq1mhJsNK2ZEgtng"
access_token = "1668962829368451073-vZbpqzVFUjQl71qK2h1e7t4gYMyEvt"
access_token_secret = "MIvqGFEvfLZyCSX9QSkTib6R32IJ4AilFtrOmXIxiLyJL"

# Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)  # Automatically wait for rate limits

# Define search keywords for Bitcoin
search_query = "Bitcoin OR #Bitcoin OR BTC OR cryptocurrency OR #cryptocurrency OR digital currency OR #digitalcurrency"

# Initialize variables for pagination
max_id = None
all_tweets = []

# Collect tweets in batches of 100 (adjust as needed)
total_collected = 0
while True:
    tweets = api.search(q=search_query, count=100, max_id=max_id)

    # Update max_id for next iteration (if there are more tweets)
    if len(tweets) > 0:
        max_id = tweets[-1].id_str  # Get the ID of the last tweet
    else:
        print("Reached end of recent tweets for this search.")
        break

    # Add tweet text to the list
    for tweet in tweets:
        all_tweets.append({"text": tweet.text})

    # Track total collected tweets
    total_collected += len(tweets)
    print(f"Collected {total_collected} tweets so far.")

    # Exit loop if rate limit is encountered (wait time included)
    if len(tweets) < 100:  # Might indicate reaching rate limit
        print("Rate limit reached, waiting...")
        time.sleep(15 * 60)  # Wait for 15 minutes (adjust as needed)
        break

# (Optional) Save the collected tweets (text) to a file for further processing
with open("bitcoin_tweets.json", "w") as outfile:
    json.dump(all_tweets, outfile)

print("Total tweets collected:", len(all_tweets))
