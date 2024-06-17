import tweepy

# Replace placeholders with your actual Twitter API credentials
consumer_key = "Wigkff1Ne9GXEtRKSQJ5MopD5"
consumer_secret = "C6a4uSNEp6HwIGRTFchEn5yQAIElGV4LhBmmew3hjL3qnbFsuu"
access_token = "1668962829368451073-sTzLiyAIGVAxGAn5fVMKHPl80LkLle"   
access_token_secret = "rNPNUcxCxc0mgmR1V8JcrYGocv98SGw8S9nfOUQHglog5"

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
