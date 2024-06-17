import tweepy

# Replace placeholders with your actual Twitter API credentials
consumer_key = "gC44j8IPEE9ipjhgl7CNbhhQd"
consumer_secret = "Qld9VTiICB7ROAGWtq0FIxA63bPDxKBVSo5o4SCJmevaEoA3CT"
access_token = "1668962829368451073-Dbt2nqjfkzOzOeoB2WGv8QHS6ftwRL"   
access_token_secret = "3uugGSLmF5Zc4lavtFqi7Xiv3r9qSEQmyAKvyLRaIOkFx"

# Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Define a StreamListener class to handle incoming tweets
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # This method is called whenever a new tweet is received
        print(f"Tweet: {status.text}")

    def on_error(self, status_code):
        # This method is called whenever an error occurs
        print(f"Error: {status_code}")

# Create a Stream object and connect the listener
stream = tweepy.Stream(auth, MyStreamListener())

# Define keywords to track (optional)
keywords = ["#programming", "python"]

# Start listening for tweets
stream.filter(track=keywords)
