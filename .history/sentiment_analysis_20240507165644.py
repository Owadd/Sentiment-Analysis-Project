from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from textblob import TextBlob

# Initialize webdriver
driver = webdriver.Chrome(ChromeDriverManager().install())

# Search query
search_term = "#cryptocurrency"

# Open Twitter search
url = f"https://twitter.com/search?q={search_term}"
driver.get(url)

# Extract tweets using scrolling
tweets = []
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(2)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

    tweets_batch = driver.find_elements(By.CSS_SELECTOR, ".tweet-text")
    tweets.extend(tweets_batch)

# Sentiment analysis on each tweet
for tweet in tweets:
    tweet_text = tweet.text.strip()  # Remove extra whitespaces
    sentiment = TextBlob(tweet_text).sentiment
    print(f"Tweet: {tweet_text}\nSentiment: {sentiment}")

# Close webdriver
driver.quit()
