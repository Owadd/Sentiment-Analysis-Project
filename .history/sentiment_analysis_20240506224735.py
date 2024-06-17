import tweepy
import json

# Set up your Twitter API credentials (replace with yours)
consumer_key = "8JDIC3wkTGvMd5jQ1tWC5DIda"
consumer_secret = "QO7TRhbEIN8oN3UADcCduEf4hj3mcboNaeQkauIiiozeK0Hnnb"
access_token = "1668962829368451073-8hUM6I2wKAwwkkLxyCPEImryJYKJ2B"
access_token_secret = "eAxz9eYMpBLXkLq1EXQxBKXlL8lah4mAjQIXcCUkWtnhZ"

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define search keywords
keywords = "bitcoin"

# Set parameters for the search query (optional)
max_results = 10  # Adjust this to retrieve a desired number of tweets
lang = "en"  # Filter for tweets in English (optional)

# Make the search request
search_results = api.search_tweets(q=keywords, count=max_results, lang=lang)

# Process and print the results
for tweet in search_results:
    print(f"Tweet Text: {tweet.text}")
    print(f"Tweet Created At: {tweet.created_at}")
    print("-" * 50)

# Alternatively, save the results to a file (modify filename as needed)
with open("tweets.json", "w") as outfile:
    json.dump(search_results, outfile)

print(f"Found {len(search_results)} tweets containing '{keywords}'.")
