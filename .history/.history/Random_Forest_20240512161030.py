import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from tqdm import tqdm
import time

def log_progress(message):
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())
    print(f"{timestamp} {message}")

try:
    # Load the dataset
    log_progress("Loading dataset...")
    df = pd.read_csv('../CSV Files/training_dataset.csv')

    # Drop rows with missing values in the 'Cleaned tweets' column
    log_progress("Dropping rows with missing values...")
    df.dropna(subset=['Cleaned tweets'], inplace=True)

    # Split the dataset into training and testing sets
    log_progress("Splitting dataset into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(df['Cleaned tweets'], df['Sentiment'], test_size=0.2, random_state=42)

    # Vectorize the tweets
    log_progress("Vectorizing tweets...")
    vectorizer = CountVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Initialize the Random Forest classifier
    log_progress("Initializing Random Forest...")
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

    # Start training and updating progress in real-time
    log_progress("Training Random Forest...")
    with tqdm(total=100, desc="Training Progress", bar_format='{l_bar}{bar}{r_bar}') as pbar:
        for _ in range(100):
            rf_classifier.partial_fit(X_train_vec, y_train, classes=['positive', 'negative', 'neutral'])
            pbar.update(1)  # Increment progress bar by 1%
            time.sleep(0.1)  # Simulate training time

    # Predict sentiment on the test set using Random Forest
    log_progress("Predicting sentiment with Random Forest...")
    with tqdm(total=len(X_test), desc="Prediction Progress", bar_format='{l_bar}{bar}{r_bar}') as pbar:
        rf_y_pred = rf_classifier.predict(X_test_vec)
        pbar.update(len(X_test))  # Increment progress bar to 100%
    rf_accuracy = accuracy_score(y_test, rf_y_pred)
    log_progress(f"Random Forest Accuracy: {rf_accuracy}")

except Exception as e:
    log_progress(f"An error occurred: {e}")
