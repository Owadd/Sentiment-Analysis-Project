import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import tweepy as tw # To extarct the twitter data
from tqdm import tqdm

consumer_api_key = '8JDIC3wkTGvMd5jQ1tWC5DIda'
consumer_api_secret = 'QO7TRhbEIN8oN3UADcCduEf4hj3mcboNaeQkauIiiozeK0Hnnb'

auth = tw.OAuthHandler(consumer_api_key, consumer_api_secret)
api = tw.API(auth, wait_on_rate_limit=True)

search_words = "bitcoin -filter:retweets" #Type you keyword here
#You can fix a time frame with the date since and date until parameters
date_since = "2024-01-01"
date_until="2024-05-07"
# Collect tweets
tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since,
              until=date_until     
              ).items(7500) #We instruct the cursor to return maximum of 7500 tweets

tweets_copy = []
for tweet in tqdm(tweets):
    tweets_copy.append(tweet)

print(f"New tweets retrieved: {len(tweets_copy)}")

for tweet in tqdm(tweets_copy):
    hashtags = []
    try:
        for hashtag in tweet.entities["hashtags"]:
            hashtags.append(hashtag["text"])
    except:
        pass
    tweets_df = tweets_df.append(pd.DataFrame({'user_name': tweet.user.name, 
                                               'user_location': tweet.user.location,\
                                               'user_description': tweet.user.description,
                                               'user_created': tweet.user.created_at,
                                               'user_followers': tweet.user.followers_count,
                                               'user_friends': tweet.user.friends_count,
                                               'user_favourites': tweet.user.favourites_count,
                                               'user_verified': tweet.user.verified,
                                               'date': tweet.created_at,
                                               'text': tweet.text, 
                                               'hashtags': [hashtags if hashtags else None],
                                               'source': tweet.source,
                                               'is_retweet': tweet.retweeted}, index=[0]))
    

tweets_df

tweets_df.to_csv('bitcoin.csv',index=False)