Sure! Here's a comprehensive README file for your "Sentiment Analysis Project" repository on GitHub.

---

# Sentiment Analysis Project

Welcome to the Sentiment Analysis Project! This repository contains scripts and data for performing sentiment analysis on tweets related to Bitcoin. Below you'll find a detailed description of the project structure, its components, and how to use them.

## Project Structure

The project is organized as follows:

```
Sentiment Analysis Project
│
├── CSV Files
│   ├── Bitcoin_tweets.csv
│   ├── cleaned_tweets.csv
│   ├── training_dataset.csv
│   ├── testing_dataset.csv
│   └── new_dataset_with_predictions.csv
│
├── label_tweets.py
├── dataset_splitter.py
├── naive_bayes_classifier.py
├── random_forest.py
├── support_vector_machine.py
├── testing_svm.py
├── twitter_scraping.py
├── twitter_sentiment_analysis_app.py
└── svm_classifier.pkl
```

### CSV Files

- **Bitcoin_tweets.csv**: Raw dataset containing tweets about Bitcoin.
- **cleaned_tweets.csv**: Cleaned dataset with additional sentiment analysis columns.
- **training_dataset.csv**: Training dataset for machine learning models.
- **testing_dataset.csv**: Testing dataset for evaluating model performance.
- **new_dataset_with_predictions.csv**: Dataset with predicted sentiments from the SVM model.

### Scripts

- **label_tweets.py**: Cleans and labels tweets based on their sentiment using TextBlob.
- **dataset_splitter.py**: Splits the cleaned dataset into training and testing sets.
- **naive_bayes_classifier.py**: Trains and evaluates a Naive Bayes classifier for sentiment analysis.
- **random_forest.py**: Trains and evaluates a Random Forest classifier for sentiment analysis.
- **support_vector_machine.py**: Trains and evaluates a Support Vector Machine (SVM) classifier for sentiment analysis.
- **testing_svm.py**: Tests the SVM model on a new dataset and evaluates its performance.
- **twitter_scraping.py**: Scrapes tweets from Twitter using Selenium and saves them to a CSV file.
- **twitter_sentiment_analysis_app.py**: A Streamlit web application for scraping tweets, cleaning data, performing sentiment analysis, and displaying results.

### Model Files

- **svm_classifier.pkl**: Trained SVM classifier model.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- Pandas
- NumPy
- Scikit-learn
- TextBlob
- Selenium
- TQDM
- Joblib
- Streamlit
- ChromeDriver

### Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/yourusername/Sentiment-Analysis-Project.git
cd Sentiment-Analysis-Project
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Usage

1. **Scrape Tweets**:
   Run the `twitter_scraping.py` script to scrape tweets about Bitcoin and save them to `Bitcoin_tweets.csv`.

   ```bash
   python twitter_scraping.py
   ```

2. **Label Tweets**:
   Run the `label_tweets.py` script to clean and label the tweets.

   ```bash
   python label_tweets.py
   ```

3. **Split Dataset**:
   Run the `dataset_splitter.py` script to split the cleaned dataset into training and testing sets.

   ```bash
   python dataset_splitter.py
   ```

4. **Train Classifiers**:
   You can train different classifiers using the provided scripts:

   - Naive Bayes Classifier:

     ```bash
     python naive_bayes_classifier.py
     ```

   - Random Forest Classifier:

     ```bash
     python random_forest.py
     ```

   - Support Vector Machine (SVM) Classifier:

     ```bash
     python support_vector_machine.py
     ```

5. **Test SVM Model**:
   Run the `testing_svm.py` script to test the SVM model on a new dataset.

   ```bash
   python testing_svm.py
   ```

6. **Streamlit Application**:
   Launch the Streamlit web application for scraping tweets, performing sentiment analysis, and displaying results.

   ```bash
   streamlit run twitter_sentiment_analysis_app.py
   ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.


## Acknowledgments

- The TextBlob library for sentiment analysis.
- The Selenium library for web scraping.
- The Scikit-learn library for machine learning algorithms.
- The Streamlit library for building the web application.

---

Feel free to customize this README file further to suit your project's needs!
