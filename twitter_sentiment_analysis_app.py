import re
import time
import csv
import joblib
import pandas as pd
import numpy as np
from tqdm import tqdm
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import matplotlib.pyplot as plt


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

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(web)
    driver.maximize_window()

    scrolling = True
    total_tweets_collected = 0
    while scrolling and total_tweets_collected < max_tweets:
        try:
            tweets = WebDriverWait(driver, 210).until(EC.presence_of_all_elements_located((By.XPATH, "//article")))
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

    driver.quit()

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
        st.success(f"Scraped {len(tweet_data)} tweets!")
        df = pd.DataFrame(tweet_data, columns=["Text"])
        df.to_csv("scraped_tweets.csv", index=False)
        st.dataframe(df)

    # Step 2: Load and clean tweets from CSV
    st.header("Load and Clean Tweets")
    if st.button("Load and Clean Tweets"):
        df = pd.read_csv('scraped_tweets.csv')

        # Drop rows where 'Text' is NaN
        df.dropna(subset=['Text'], inplace=True)

        # Apply cleaning function
        df['Text'] = df['Text'].apply(lambda x: clean_tweet(x) if isinstance(x, str) else "")

        st.success("Tweets loaded and cleaned!")
        st.dataframe(df)

    # Step 3: Perform sentiment analysis
    st.header("Perform Sentiment Analysis")
    if st.button("Perform Sentiment Analysis"):
        df = pd.read_csv('scraped_tweets.csv')

        # Drop rows where 'Text' is NaN
        df.dropna(subset=['Text'], inplace=True)

        st.text("Loading saved vectorizer and SVM classifier...")
        vectorizer = joblib.load('vectorizer.pkl')
        svm_classifier = joblib.load('svm_classifier.pkl')

        st.text("Vectorizing new data...")
        X_new = df['Text'].tolist()
        X_new_vec = vectorizer.transform(tqdm(X_new, desc="Vectorizing"))

        st.text("Predicting sentiment...")
        y_pred = svm_classifier.predict(X_new_vec)
        df['Predicted Sentiment'] = y_pred
        df.to_csv('new_dataset_with_predictions.csv', index=False)

        st.success("Sentiment analysis complete and predictions saved!")
        st.dataframe(df)

    # Step 4: Generate sentiment score and summaries
    st.header("Sentiment Score and Summaries")
    if st.button("Generate Sentiment Score and Summaries"):
        df = pd.read_csv('new_dataset_with_predictions.csv')
        sentiment_counts = df['Predicted Sentiment'].value_counts()
        positive_count = sentiment_counts.get('positive', 0)
        negative_count = sentiment_counts.get('negative', 0)
        total_count = positive_count + negative_count
        sentiment_score = (positive_count - negative_count) / total_count if total_count > 0 else 0

        st.success(f"Sentiment Score: {sentiment_score:.2f}")

        df['Text Length'] = df['Text'].apply(len)
        top_positive_tweets = df[df['Predicted Sentiment'] == 'positive'].sort_values(by='Text Length',
                                                                                      ascending=False).head(3)
        top_negative_tweets = df[df['Predicted Sentiment'] == 'negative'].sort_values(by='Text Length',
                                                                                      ascending=False).head(3)

        st.subheader("Top Positive Tweets")
        for tweet in top_positive_tweets['Text']:
            st.write(f"- {tweet}")

        st.subheader("Top Negative Tweets")
        for tweet in top_negative_tweets['Text']:
            st.write(f"- {tweet}")

        # Step 5: Generate pie chart
        st.subheader("Sentiment Analysis Results")
        labels = ['Positive', 'Negative']
        sizes = [positive_count, negative_count]
        colors = ['#1f77b4', '#ff7f0e']
        explode = (0.1, 0)  # explode the 1st slice (i.e. 'Positive')

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(sizes, explode=explode, labels=labels, colors=colors,
               autopct='%1.1f%%', shadow=True, startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title('Sentiment Analysis Results')
        st.pyplot(fig)


if __name__ == '__main__':
    main()
