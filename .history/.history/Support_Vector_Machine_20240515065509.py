import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

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

    # Extract features and labels
    X_new = df['Cleaned tweets']
    y_true = df['Sentiment']

    # Vectorize the new data
    print("Vectorizing new data...")
    X_new_vec = vectorizer.transform(X_new)

    # Predict sentiment using the loaded SVM classifier
    print("Predicting sentiment...")
    y_pred = svm_classifier.predict(X_new_vec)

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

    # Save the results to a new CSV file
    df['Predicted Sentiment'] = y_pred
    df.to_csv('new_dataset_with_predictions.csv', index=False)
    print("Predictions saved to 'new_dataset_with_predictions.csv'")

except Exception as e:
    print("An error occurred:", e)
