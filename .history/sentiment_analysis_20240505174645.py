import tweepy


consumer_key = "gC44j8IPEE9ipjhgl7CNbhhQd"
consumer_secret = "Qld9VTiICB7ROAGWtq0FIxA63bPDxKBVSo5o4SCJmevaEoA3CT"
access_token = "1668962829368451073-Dbt2nqjfkzOzOeoB2WGv8QHS6ftwRL"   
access_token_secret = "3uugGSLmF5Zc4lavtFqi7Xiv3r9qSEQmyAKvyLRaIOkFx"



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets: 
    print (tweet.text)