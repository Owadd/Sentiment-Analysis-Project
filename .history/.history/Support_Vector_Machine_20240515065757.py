import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tqdm import tqdm
import joblib
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

    # Vectorize the tweets with progress bar
    print("Vectorizing tweets...")
    vectorizer = CountVectorizer()
    with tqdm(total=len(X_train)) as pbar:
        X_train_vec = vectorizer.fit_transform(X_train)
        pbar.update(len(X_train))

    with tqdm(total=len(X_test)) as pbar:
        X_test_vec = vectorizer.transform(X_test)
        pbar.update(len(X_test))

    # Initialize and train the SVM classifier
    print("Training SVM...")
    start_time = time.time()
    svm_classifier = SVC(kernel='linear')
    svm_classifier.fit(X_train_vec, y_train)
    end_time = time.time()

    # Save the trained vectorizer and SVM classifier to files
    print("Saving trained objects...")
    joblib.dump(vectorizer, 'vectorizer.pkl')
    joblib.dump(svm_classifier, 'svm_classifier.pkl')

    # Predict sentiment on the test set using SVM
    print("Predicting sentiment with SVM...")
    svm_y_pred = svm_classifier.predict(X_test_vec)

    # Calculate accuracy
    svm_accuracy = accuracy_score(y_test, svm_y_pred)
    print("SVM Accuracy:", svm_accuracy)

    # Calculate precision, recall, and F1 score
    precision = precision_score(y_test, svm_y_pred, average='weighted')
    recall = recall_score(y_test, svm_y_pred, average='weighted')
    f1 = f1_score(y_test, svm_y_pred, average='weighted')

    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1)

    # Print training time
    total_time = end_time - start_time
    print("Total training time: {:.2f} seconds".format(total_time))

except Exception as e:
    print("An error occurred:", e)
