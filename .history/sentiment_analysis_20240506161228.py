import tweepy


api_key = 'Wigkff1Ne9GXEtRKSQJ5MopD5'
api_secret = 'C6a4uSNEp6HwIGRTFchEn5yQAIElGV4LhBmmew3hjL3qnbFsuu'
access_token = '1668962829368451073-sTzLiyAIGVAxGAn5fVMKHPl80LkLle'
access_token_secret = 'rNPNUcxCxc0mgmR1V8JcrYGocv98SGw8S9nfOUQHglog5'

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create a listener class to handle streamed tweets
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # Print the text of the tweet and any hashtags it contains
        print(f"Text: {status.text}")
        print(f"Hashtags: {', '.join([hashtag['text'] for hashtag in status.entities['hashtags']])}")
        print("-" * 40)

    def on_error(self, status_code):
        # Handle errors during streaming
        print(f"Error: {status_code}")

# Create a stream object and filter tweets by keywords
stream = tweepy.Stream(auth, MyStreamListener())
stream.filter(track=["Bitcoin", "#BTC"])

# This code will continue to stream tweets until manually stopped