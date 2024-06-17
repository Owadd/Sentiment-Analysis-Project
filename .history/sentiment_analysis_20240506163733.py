import tweepy


consumer_key = 'Wigkff1Ne9GXEtRKSQJ5MopD5'
consumer_secret = 'C6a4uSNEp6HwIGRTFchEn5yQAIElGV4LhBmmew3hjL3qnbFsuu'
access_token = '1668962829368451073-sTzLiyAIGVAxGAn5fVMKHPl80LkLle'
access_token_secret = 'rNPNUcxCxc0mgmR1V8JcrYGocv98SGw8S9nfOUQHglog5'

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create a stream object with minimal logic in the main program
def on_status(status):
    # Print the text of the tweet and any hashtags it contains
    print(f"Text: {status.text}")
    print(f"Hashtags: {', '.join([hashtag['text'] for hashtag in status.entities['hashtags']])}")
    print("-" * 40)

def on_error(status_code):
    # Handle errors during streaming
    print(f"Error: {status_code}")

stream = tweepy.Stream(consumer_key,consumer_secret,access_token,access_token_secret)
stream.filter(track=["Bitcoin", "#BTC"])

# This code will continue to stream tweets until manually stopped