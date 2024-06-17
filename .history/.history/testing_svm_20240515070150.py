import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
from tqdm import tqdm
import time

try:
    # Load the saved vectorizer and SVM classifier
    print("Loading saved vectorizer and SVM classifier...")
    vectorizer = joblib.load('vectorizer.pkl')
    svm_classifier = joblib.load('svm_classifier.pkl')

    # Load the new dataset for testing
    print("Loading new dataset for testing...")
    df = pd.read_csv('../CSV Files/testing_dataset.csv')

    # Drop rows with missing values in the 'Cleaned tweets' column
    print("Removing missing values...")
    df.dropna(subset=['Cleaned tweets'], inplace=True)

    # Additional step: remove rows where 'Cleaned tweets' is empty after stripping whitespace
    df['Cleaned tweets'] = df['Cleaned tweets'].str.strip()  # Remove leading/trailing whitespace
    df = df[df['Cleaned tweets'] != '']  # Remove rows with empty strings

    # Extract features and labels
    X_new = df['Cleaned tweets']
    y_true = df['Sentiment']

    # Vectorize the new data with a progress bar
    print("Vectorizing new data...")
    start_time = time.time()
    X_new_vec = vectorizer.transform(tqdm(X_new, desc="Vectorizing data"))

    # Predict sentiment using the loaded SVM classifier with progress bar and countdown
    print("Predicting sentiment...")
    y_pred = []
    with tqdm(total=len(X_new_vec), desc="Predicting sentiment") as pbar:
        for i, vec in enumerate(X_new_vec):
            if i > 0:
                elapsed_time = time.time() - start_time
                remaining_time = elapsed_time * (len(X_new_vec) - i) / i
                pbar.set_postfix_str(f"ETA: {remaining_time:.2f}s")
            y_pred.append(svm_classifier.predict(vec))
            pbar.update(1)
    y_pred = [item for sublist in y_pred for item in sublist]  # Flatten the list of predictions

    # Calculate accuracy
    accuracy = accuracy_score(y_true, y_pred)
    print("Accuracy:", accuracy)

    # Calculate precision, recall, and F1 score
    precision = precision_score(y_true, y_pred, average='weighted')
    recall = recall_score(y_true, y_pred, average='weighted')
    f1 = f1_score(y_true, y_pred, average='weighted')

    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1)

    # Print testing time
    total_time = time.time() - start_time
    print("Total testing time: {:.2f} seconds".format(total_time))

    # Save the results to a new CSV file
    df['Predicted Sentiment'] = y_pred
    df.to_csv('new_dataset_with_predictions.csv', index=False)
    print("Predictions saved to 'new_dataset_with_predictions.csv'")

except Exception as e:
    print("An error occurred:", e)
