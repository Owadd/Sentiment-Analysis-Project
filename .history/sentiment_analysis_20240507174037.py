from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


web = 'https://twitter.com/search?q=bitcoin&src=typed_query'
path = "/Users/Michael/Documents/Sentiment Analysis Project/chromedriver_win32"
driver = webdriver.Chrome()
driver.get(web)
driver.maximize_window()
time.sleep(6)

username_field = driver.find_element("xpath", "//input[@name='text']")
username_field.send_keys("@Owad_of_Bubble")  # Replace 'your_username' with your actual username

next_button = driver.find_element("xpath", '//div[@role="button"]//span[text()="Next"]')
next_button.click()
time.sleep(3)

password_field = driver.find_element("xpath", "//input[@name='password']")
password_field.send_keys("@Thanksgiving001") # Replace 'YourPassword' with your actual password

login_button = driver.find_element("xpath", "//div[@role='button']//span[text()='Log in']")
login_button.click()
time.sleep(3)

def get_tweet(element):
    try:
        user = element.find_element("xpath", ".//*[contains(text(), '@')]").text
        text = element.find_element("xpath", ".//div[@lang]").text
        tweet_data = [user, text]
        return tweet_data
    except Exception as e:
        print(f"Error: {e}")
        return None

user_data = []
text_data = []
tweet_ids = set()

scrolling = True
while scrolling:
    tweets = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//article")))
    for tweet in tweets[-15:]:
        tweet_list = get_tweet(tweet)
        if tweet_list:
            tweet_id = ''.join(tweet_list)
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                user_data.append(tweet_list[0])
                text_data.append(" ".join(tweet_list[1].split()))

    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        scrolling = False
    else:
        last_height = new_height

driver.quit()

# Creating DataFrame
df = pd.DataFrame({'User': user_data, 'Text': text_data})
print(df)
