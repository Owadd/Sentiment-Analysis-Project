import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

try:
    # Load the dataset
    df = pd.read_csv('training_data.csv')

    # Drop rows with missing values in the 'Cleaned tweets' column
    df.dropna(subset=['Cleaned tweets'], inplace=True)

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df['Cleaned tweets'], df['Sentiment'], test_size=0.2, random_state=42)

    # Vectorize the tweets
    vectorizer = CountVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Initialize and train the Random Forest classifier
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_classifier.fit(X_train_vec, y_train)

    # Predict sentiment on the test set using Random Forest
    rf_y_pred = rf_classifier.predict(X_test_vec)
    rf_accuracy = accuracy_score(y_test, rf_y_pred)
    print("Random Forest Accuracy:", rf_accuracy)

except Exception as e:
    print("An error occurred:", e)