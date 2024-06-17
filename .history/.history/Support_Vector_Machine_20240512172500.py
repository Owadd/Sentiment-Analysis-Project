import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from tqdm import tqdm
import time

try:
    # Load the dataset
    print("Loading dataset...")
    df = pd.read_csv('../CSV Files/training_dataset.csv')

    # Drop rows with missing values in the 'Cleaned tweets' column
    print("Removing missing values...")
    df.dropna(subset=['Cleaned tweets'], inplace=True)

    # Split the dataset into training and testing sets
    print("Splitting dataset into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(df['Cleaned tweets'], df['Sentiment'], test_size=0.2, random_state=42)

    # Vectorize the tweets
    print("Vectorizing tweets...")
    vectorizer = CountVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Initialize and train the SVM classifier
    print("Training SVM...")
    svm_classifier = SVC(kernel='linear')
    svm_classifier.fit(X_train_vec, y_train)

    # Predict sentiment on the test set using SVM
    print("Predicting sentiment with SVM...")
    svm_y_pred = svm_classifier.predict(X_test_vec)
    svm_accuracy = accuracy_score(y_test, svm_y_pred)
    print("SVM Accuracy:", svm_accuracy)

except Exception as e:
    print("An error occurred:", e)
