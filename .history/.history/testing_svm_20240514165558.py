import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from tqdm import tqdm
import joblib

try:
    # Load the new dataset
    print("Loading new dataset...")
    new_df = pd.read_csv('../CSV Files/testing_dataset.csv')

    # Assuming 'Cleaned tweets' column is present in the new dataset
    if 'Cleaned tweets' not in new_df.columns:
        raise ValueError("Column 'Cleaned tweets' not found in the new dataset.")

    new_tweets = new_df['Cleaned tweets']

    # Load the trained vectorizer
    print("Loading vectorizer...")
    vectorizer = joblib.load('vectorizer.pkl')

    # Vectorize the new tweets
    print("Vectorizing new tweets...")
    new_tweets_vec = vectorizer.transform(new_tweets)

    # Load the trained SVM classifier
    print("Loading SVM classifier...")
    svm_classifier = joblib.load('svm_classifier.pkl')

    # Predict sentiment on the new dataset using SVM
    print("Predicting sentiment on new dataset with SVM...")
    new_y_pred = svm_classifier.predict(new_tweets_vec)

    # If ground truth labels are available in the new dataset, calculate accuracy
    if 'Sentiment' in new_df.columns:
        new_y_true = new_df['Sentiment']
        new_accuracy = accuracy_score(new_y_true, new_y_pred)
        print("Accuracy on new dataset:", new_accuracy)
    else:
        print("Ground truth labels not available in the new dataset.")

except FileNotFoundError:
    print("Error: The file path provided does not exist.")
except ValueError as ve:
    print("ValueError occurred:", ve)
except Exception as e:
    print("An error occurred:", e)
