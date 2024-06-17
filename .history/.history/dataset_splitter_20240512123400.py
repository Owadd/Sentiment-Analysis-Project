import pandas as pd

# Replace 'your_sentiment_file.csv' with the actual filename
data_file = "../CSV Files/cleaned_tweets.csv"

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv(data_file)

# Shuffle the DataFrame for randomness (important!)
df = df.sample(frac=1)

# Calculate split points (assuming a sentiment label column named 'sentiment')
split_point = int(0.8 * len(df))
train_data = df[0:split_point]
test_data = df[split_point:]

# Optional: Save the split data to separate CSV files
train_data.to_csv("../CSV Files/training_dataset.csv", index=False)
test_data.to_csv("../CSV Files/testing_dataset.csv", index=False)

print("Data split complete!")
print(f"Training data size: {len(train_data)}")
print(f"Testing data size: {len(test_data)}")
