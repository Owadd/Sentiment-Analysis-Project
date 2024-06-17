import re
import time
import csv
import joblib
import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def clean_tweet(text):
    """
    This function cleans a tweet by removing hashtags, mentions, URLs, and punctuation.
    """
    text = text.lower()
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = " ".join(text.split())
    return text

try:
    # Step 1: Scrape tweets
    
    
    search_term = "Bitcoin"
    web = f"https://twitter.com/search?q={search_term}&src=typed_query"
    path = "/Users/Michael/Documents/Sentiment Analysis Project/chromedriver_win32"

    def get_tweet_data(tweet_element):
        try:
            tweet_text = tweet_element.find_element(By.XPATH, ".//div[@lang]").text.strip()
            return tweet_text
        except Exception as e:
            print(f"Error extracting tweet data: {e}")
            return None

    text_data = []
    tweet_ids = set()

    csv_file = open("scraped_tweets.csv", "w", newline="", encoding="utf-8")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Text"])

    driver = webdriver.Chrome()
    driver.get(web)
    driver.maximize_window()

    scrolling = True
    total_tweets_collected = 0
    while scrolling and total_tweets_collected < 100:
        try:
            tweets = WebDriverWait(driver, 210).until(EC.presence_of_all_elements_located((By.XPATH, "//article")))
            for tweet in tweets:
                tweet_data = get_tweet_data(tweet)
                if tweet_data:
                    if tweet_data not in tweet_ids:
                        tweet_ids.add(tweet_data)
                        cleaned_tweet = clean_tweet(tweet_data)  # Clean the tweet before saving
                        text_data.append(cleaned_tweet)
                        csv_writer.writerow([cleaned_tweet])
                        total_tweets_collected += 1
                        if total_tweets_collected >= 100:
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
    csv_file.close()

    print("Tweet data saved to scraped_tweets.csv")

    # Step 2: Load and clean tweets from CSV
    df = pd.read_csv('scraped_tweets.csv')

    # Remove NaN values
    df['Text'].dropna(inplace=True)

    # Step 3: Perform sentiment analysis
    print("Loading saved vectorizer and SVM classifier...")
    vectorizer = joblib.load('vectorizer.pkl')
    svm_classifier = joblib.load('svm_classifier.pkl')

    print("Vectorizing new data...")
    X_new = df['Text'].tolist()
    X_new_vec = vectorizer.transform(tqdm(X_new, desc="Vectorizing"))

    print("Predicting sentiment...")
    y_pred = svm_classifier.predict(X_new_vec)
    df['Predicted Sentiment'] = y_pred

    df.to_csv('new_dataset_with_predictions.csv', index=False)
    print("Predictions saved to 'new_dataset_with_predictions.csv'")

    # Step 4: Generate sentiment score and summaries
    sentiment_counts = df['Predicted Sentiment'].value_counts()
    positive_count = sentiment_counts.get('positive', 0)
    negative_count = sentiment_counts.get('negative', 0)
    total_count = positive_count + negative_count
    sentiment_score = (positive_count - negative_count) / total_count if total_count > 0 else 0

    print(f"Sentiment Score: {sentiment_score:.2f}")

    # Add length column to sort by tweet length
    df['Text Length'] = df['Text'].apply(len)
    top_positive_tweets = df[df['Predicted Sentiment'] == 'positive'].sort_values(by='Text Length', ascending=False).head(3)
    top_negative_tweets = df[df['Predicted Sentiment'] == 'negative'].sort_values(by='Text Length', ascending=False).head(3)

    print("\nTop Positive Tweets:")
    for tweet in top_positive_tweets['Text']:
        print(f"- {tweet}")

    print("\nTop Negative Tweets:")
    for tweet in top_negative_tweets['Text']:
        print(f"- {tweet}")

    # Step 5: Generate pie chart
    plt.figure(figsize=(8, 8))
    labels = ['Positive', 'Negative']
    sizes = [positive_count, negative_count]
    colors = ['#1f77b4', '#ff7f0e']
    explode = (0.1, 0)  # explode the 1st slice (i.e. 'Positive')

    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Sentiment Analysis Results')
    plt.show()
     

except Exception as e:
    print("An error occurred:", e)
