import os
import subprocess

# Run the setup.sh script to set permissions for chromedriver
subprocess.call(['chmod', '+x', './chromedriver-win64/chromedriver-win64/chromedriver.exe'])

# Imports
import re
import logging
import time
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import streamlit as st

# Function to clean tweets
def clean_tweet(text):
    if text is None:
        return ""
    text = text.lower()
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = " ".join(text.split())
    return text

# Function to scrape tweets
def scrape_tweets(search_term, max_tweets):
    web = f"https://twitter.com/search?q={search_term}&src=typed_query"

    def get_tweet_data(tweet_element):
        try:
            tweet_text = tweet_element.find_element(By.XPATH, ".//div[@lang]").text.strip()
            return tweet_text
        except Exception as e:
            print(f"Error extracting tweet data: {e}")
            return None

    text_data = []
    tweet_ids = set()

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(web)

    scrolling = True
    total_tweets_collected = 0
    while scrolling and total_tweets_collected < max_tweets:
        try:
            tweets = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//article")))
            for tweet in tweets:
                tweet_data = get_tweet_data(tweet)
                if tweet_data:
                    if tweet_data not in tweet_ids:
                        tweet_ids.add(tweet_data)
                        cleaned_tweet = clean_tweet(tweet_data)  # Clean the tweet before saving
                        text_data.append(cleaned_tweet)
                        total_tweets_collected += 1
                        if total_tweets_collected >= max_tweets:
                            break
            last_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                scrolling = False
        except TimeoutException:
            print("Timeout waiting for elements. Stopping scraping.")
            scrolling = False
        except Exception as e:
            print(f"Unexpected error: {e}")
            scrolling = False

    driver.quit()

    print(f"Scraped {len(text_data)} tweets")
    return text_data

# Streamlit app
def main():
    st.title("Twitter Sentiment Analysis")

    # Step 1: User input for scraping tweets
    st.header("Scrape Tweets")
    search_term = st.text_input("Enter the search term:", "Bitcoin")
    max_tweets = st.number_input("Enter the number of tweets to scrape:", min_value=10, max_value=1000, value=100)
    scrape_button = st.button("Scrape Tweets")

    if scrape_button:
        with st.spinner("Scraping tweets..."):
            tweet_data = scrape_tweets(search_term, max_tweets)
        if tweet_data is not None:
            st.success(f"Scraped {len(tweet_data)} tweets!")
            df = pd.DataFrame(tweet_data, columns=["Text"])
            st.dataframe(df)
        else:
            st.error("Failed to scrape tweets.")

    # Step 2: Load and clean tweets from CSV
    st.header("Load and Clean Tweets")
    if st.button("Load and Clean Tweets"):
        df = pd.DataFrame(tweet_data, columns=["Text"])
        df['Text'] = df['Text'].apply(clean_tweet)
        st.success("Tweets loaded and cleaned!")
        st.dataframe(df)

if __name__ == '__main__':
    main()
