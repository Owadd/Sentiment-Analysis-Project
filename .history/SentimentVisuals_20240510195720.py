import matplotlib.pyplot as plt
import csv

# Define file path (replace with the actual path to your CSV)
data_file = "./training_dataset.csv"  # Update with your file path
sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}

# Read sentiment data from CSV
with open(data_file, 'r', encoding="utf-8") as infile:
  reader = csv.DictReader(infile)
  for row in reader:
    sentiment = row["Sentiment"]
    sentiment_counts[sentiment] += 1

# Extract sentiment labels and counts
sentiment_labels = list(sentiment_counts.keys())
sentiment_values = list(sentiment_counts.values())

# Create bar chart
plt.figure(figsize=(8, 6))  # Adjust figure size as needed
plt.bar(sentiment_labels, sentiment_values, color=['green', 'red', 'gray'])
plt.xlabel("Sentiment")
plt.ylabel("Tweet Count")
plt.title("Sentiment Distribution of Tweets")
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()

# Display the chart
plt.show()

print("Sentiment distribution visualized in the bar chart.")
