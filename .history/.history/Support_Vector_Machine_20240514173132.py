import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tqdm import tqdm
import joblib
import time

def get_time_remaining(start_time, progress, total_progress):
    elapsed_time = time.time() - start_time
    if progress == 0:
        return 'Calculating...'
    time_per_progress = elapsed_time / progress
    remaining_progress = total_progress - progress
    time_remaining = remaining_progress * time_per_progress
    return time_remaining

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

    # Initialize SVM classifier
    print("Initializing SVM classifier...")
    svm_classifier = SVC(kernel='linear')

    # Initialize progress bar
    total_progress = 100
    with tqdm(total=total_progress, desc="Training SVM", position=0) as pbar:
        start_time = time.time()
        svm_classifier.fit(X_train_vec, y_train)
        end_time = time.time()
        pbar.update(total_progress)

    # Save the trained objects
    print("Saving trained objects...")
    joblib.dump(vectorizer, 'vectorizer.pkl')
    joblib.dump(svm_classifier, 'svm_classifier.pkl')

    # Predict sentiment on the test set using SVM
    print("Predicting sentiment with SVM...")
    svm_y_pred = svm_classifier.predict(X_test_vec)

    # Calculate evaluation metrics
    svm_accuracy = accuracy_score(y_test, svm_y_pred)
    precision = precision_score(y_test, svm_y_pred, average='weighted')
    recall = recall_score(y_test, svm_y_pred, average='weighted')
    f1 = f1_score(y_test, svm_y_pred, average='weighted')

    print("SVM Accuracy:", svm_accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1)

    # Print training time and estimated time remaining
    total_time = end_time - start_time
    time_remaining = get_time_remaining(start_time, total_progress, total_progress)
    print("Total training time: {:.2f} seconds".format(total_time))
    print("Estimated time remaining: {:.2f} seconds".format(time_remaining))

except Exception as e:
    print("An error occurred:", e)
