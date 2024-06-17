import tweepy

# Define Twitter API credentials 
consumer_key = "gC44j8IPEE9ipjhgl7CNbhhQd"
consumer_secret = "Qld9VTiICB7ROAGWtq0FIxA63bPDxKBVSo5o4SCJmevaEoA3CT"
access_token = "1668962829368451073-Dbt2nqjfkzOzOeoB2WGv8QHS6ftwRL"
access_token_secret = "3uugGSLmF5Zc4lavtFqi7Xiv3r9qSEQmyAKvyLRaIOkFx"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create a class inheriting from StreamListener
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)

# Create an instance of MyStreamListener
myStreamListener = MyStreamListener()

# Create a Stream object
myStream = tweepy.Stream(auth=auth, listener=myStreamListener)

# Start streaming tweets containing the word "python"
myStream.filter(track=['Bitcoin','#BTC'])