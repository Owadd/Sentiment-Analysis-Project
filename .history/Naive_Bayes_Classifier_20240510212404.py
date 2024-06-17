import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer
import pandas as pd


# Replace 'sentiment_training_data.csv' with your actual filename
train_data_file = "./training_dataset.csv"

# Load the training data
data = pd.read_csv(train_data_file)

# Assuming sentiment is in a column named 'sentiment' and tweets are in a column named 'text' (replace with actual names)
tweets = data["Cleaned tweets"]
sentiment_labels = data["Sentiment"]


def preprocess_text(text):
  """Function to preprocess text data for sentiment analysis using NLTK

  Args:
      text: String containing the text to be preprocessed

  Returns:
      String: The preprocessed text
  """
  # Download NLTK resources (run only once at the beginning)
  # nltk.download('punkt')
  # nltk.download('stopwords')

  # Tokenization (split text into words)
  tokens = nltk.word_tokenize(text)

  # Lowercase conversion
  tokens = [token.lower() for token in tokens]

  # Optional: Stop word removal
  stop_words = stopwords.words('english')
  tokens = [token for token in tokens if token not in stop_words]

  # Optional: Stemming (reduce words to base form)
  # stemmer = PorterStemmer()
  # tokens = [stemmer.stem(token) for token in tokens]

  # Remove punctuation (you can replace with regular expressions if preferred)
  tokens = [word for word in tokens if word.isalpha()]

  # Join preprocessed tokens back into text
  preprocessed_text = ' '.join(tokens)
  return preprocessed_text

# Preprocess text data
tweets_preprocessed = [preprocess_text(text) for text in tweets]


# KNN Imputation for handling missing values in preprocessed text data
imputer = KNNImputer(n_neighbors=5)  # Adjust n_neighbors as needed
tweets_transformed = imputer.fit_transform(tweets_preprocessed.values.reshape(-1, 1))

# Feature extraction using TF-IDF vectorizer
vectorizer = TfidfVectorizer(max_features=2000)  # Adjust max_features as needed
features = vectorizer.fit_transform(tweets_transformed)

# Train-Test split within the training data (optional for hyperparameter tuning)
X_train, X_val, y_train, y_val = train_test_split(features, sentiment_labels, test_size=0.1, random_state=42)

# Train the Naive Bayes model
model = MultinomialNB()
model.fit(X_train, y_train)

# Optional: Evaluate the model on the validation set (X_val, y_val) using metrics like accuracy or F1 score

print("Model training complete!")
