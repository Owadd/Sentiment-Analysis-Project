from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import csv

# Search query
search_term = "bitcoin"

# Define URL with search query
web = f"https://twitter.com/search?q={search_term}&src=typed_query"

# Path to ChromeDriver (adjust accordingly)
path = "/Users/Michael/Documents/Sentiment Analysis Project/chromedriver_win32"

def get_tweet_data(tweet_element):
    """Extracts username and tweet text from a tweet element.

    Args:
        tweet_element (WebElement): The tweet element to extract data from.

    Returns:
        list: A list containing username and tweet text (cleaned), or None if an error occurs.
    """
    try:
        # Extract username (adapt XPath if necessary)
        username = tweet_element.find_element(By.XPATH, ".//*[contains(text(), '@')]").text

        # Extract tweet text (clean and remove extra whitespaces)
        tweet_text = tweet_element.find_element(By.XPATH, ".//div[@lang]").text.strip()
        return [username, tweet_text]
    except Exception as e:
        print(f"Error extracting tweet data: {e}")
        return None

# Lists to store extracted data
user_data = []
text_data = []
tweet_ids = set()

# CSV file setup
csv_file = open("extracted_tweets.csv", "w", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["User", "Text"])  # Write headers

# Set up webdriver
driver = webdriver.Chrome()
driver.get(web)
driver.maximize_window()

# Scrolling and data extraction loop
scrolling = True
while scrolling:
    try:
        # Wait for tweets to load (adjust timeout if needed)
        tweets = WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located((By.XPATH, "//article")))

        # Process the last 15 tweets (adjust as needed)
        for tweet in tweets[-15:]:
            tweet_data = get_tweet_data(tweet)
            if tweet_data:
                tweet_id = ''.join(tweet_data)
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    user_data.append(tweet_data[0])
                    text_data.append(tweet_data[1])
                    csv_writer.writerow(tweet_data)  # Write data to CSV

        # Scroll down and check for new content
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")

        # Stop scrolling if no new content is loaded
        if new_height == last_height:
            scrolling = False
    except TimeoutException:
        print("Timeout waiting for elements. Stopping scraping.")
        scrolling = False

# Close browser window and CSV file
driver.quit()
csv_file.close()

print("Tweet data saved to extracted_tweets.csv")
