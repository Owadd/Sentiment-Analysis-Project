import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from tqdm import tqdm
import time

try:
    # Load the dataset
    df = pd.read_csv('../CSV Files/training_dataset.csv')

    # Drop rows with missing values in the 'Cleaned tweets' column
    df.dropna(subset=['Cleaned tweets'], inplace=True)

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df['Cleaned tweets'], df['Sentiment'], test_size=0.2, random_state=42)

    # Vectorize the tweets
    vectorizer = CountVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Initialize and train the Naive Bayes classifier
    nb_classifier = MultinomialNB()
    nb_classifier.fit(X_train_vec, y_train)

    # Predict sentiment on the test set
    y_pred = []
    total_test_samples = X_test_vec.shape[0]
    progress_bar = tqdm(total=total_test_samples, desc="Testing Progress", unit="samples")

    for i in range(total_test_samples):
        # Predict sentiment for each test sample
        y_pred.append(nb_classifier.predict(X_test_vec[i]))
        time.sleep(0.01)  # Simulate some computation
        progress_bar.update(1)  # Update progress bar

    # Close progress bar
    progress_bar.close()

    # Calculate accuracy
    y_pred = np.array(y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    print("Naive Bayes Classifier Accuracy:", accuracy)

except Exception as e:
    print("An error occurred:", e)
