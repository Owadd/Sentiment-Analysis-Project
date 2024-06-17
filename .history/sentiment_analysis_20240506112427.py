import tweepy
import json
import csv
from kafka import KafkaProducer

api_key = 'Wigkff1Ne9GXEtRKSQJ5MopD5'
api_secret = 'C6a4uSNEp6HwIGRTFchEn5yQAIElGV4LhBmmew3hjL3qnbFsuu'
access_token = '1668962829368451073-sTzLiyAIGVAxGAn5fVMKHPl80LkLle'
access_token_secret = 'rNPNUcxCxc0mgmR1V8JcrYGocv98SGw8S9nfOUQHglog5'

kafka_bootstrap_server = 'localhost:9092'
kafka_topic = 'twitter_data'

csv_output = 'filepath/twitter-data-from-api.csv'

kafka_producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_server)

class TweetStreamListener(tweepy.Stream):
    def on_status(self, status):
        try:
            tweet_id = status.id
            tweet_text = status.text
            tweet_created = status.created_at.strftime('%Y-%m-%d %H:%M:%S')

            tweet_data = {
                'id': tweet_id,
                'text': tweet_text,
                'created at': tweet_created
            }

            kafka_producer.send(kafka_topic,
                                json.dumps(tweet_data).encode("UTF-8"),
                                api_version=(3, 5, 0))

            with open(csv_output, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows([[tweet_id, tweet_text, tweet_created]])

        except Exception as e:
            print(f"Error: {str(e)}")

def extract_data():
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    twitter_stream_listener = TweetStreamListener(api.auth, None)
    stream = tweepy.Stream(auth=api.auth, listener=twitter_stream_listener)

    stream.filter(['Key1', 'Key2', 'Key3'])

    kafka_producer.close()

extract_data()