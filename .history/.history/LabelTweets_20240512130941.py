from textblob import TextBlob
import csv
import re

try:
    # Define file paths
    input_file = "../Bitcoin_tweets.csv/Bitcoin_tweets.csv"  # Replace with your actual file path
    output_file = "../CSV Files/cleaned_tweets.csv"

    # Define sentiment thresholds
    positive_threshold = 0.2
    negative_threshold = -0.2

    def clean_tweet(text):
      """
      This function cleans a tweet by removing hashtags, mentions, URLs, and punctuation.
      """
      # Lowercase for case-insensitivity
      text = text.lower()
      # Remove hashtags
      text = re.sub(r"#\w+", "", text)
      # Remove mentions
      text = re.sub(r"@\w+", "", text)
      # Remove URLs
      text = re.sub(r"http\S+", "", text)
      # Remove punctuation
      text = re.sub(r"[^\w\s]", "", text)
      # Remove extra spaces
      text = " ".join(text.split())
      return text

    def classify_sentiment(polarity):
      """
      This function classifies sentiment based on a polarity threshold.
      """
      if polarity > positive_threshold:
        return "positive"
      elif polarity < negative_threshold:
        return "negative"
      else:
        return "neutral"

    with open(input_file, 'r', encoding="utf-8") as infile, open(output_file, 'w', encoding="utf-8", newline='') as outfile:
      reader = csv.DictReader(infile)
      writer = csv.DictWriter(outfile, fieldnames=["Cleaned tweets", "Polarity", "Subjectivity", "Sentiment"])
      writer.writeheader()

      for row in reader:
        # Clean the tweet text
        cleaned_text = clean_tweet(row["text"])
        # Perform sentiment analysis
        blob = TextBlob(cleaned_text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        # Classify sentiment
        sentiment = classify_sentiment(polarity)

        # Write data to new CSV with desired columns
        writer.writerow({
          "Cleaned tweets": cleaned_text,
          "Polarity": polarity,
          "Subjectivity": subjectivity,
          "Sentiment": sentiment
        })

    print(f"Sentiment analysis completed. Results saved to {output_file}")

except FileNotFoundError:
    print("Error: The file specified was not found.")
except csv.Error:
    print("Error: There was an issue with reading or writing the CSV file.")
except Exception as e:
    print("An unexpected error occurred:", str(e))
