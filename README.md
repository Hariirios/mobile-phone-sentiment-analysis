# Mobile Phone Review Sentiment Analysis

This project implements a sentiment analysis application for mobile phone reviews using machine learning.

## Features

- Real-time sentiment prediction for mobile phone reviews
- Preprocessing of text data (lowercasing, removing punctuation, stopword removal, lemmatization)
- Streamlit-based web interface for easy interaction

## Files

- `app.py`: Main Streamlit application
- `sentiment_model.pkl`: Trained sentiment classification model
- `tfidf_vectorizer.pkl`: TF-IDF vectorizer for text preprocessing
- `data_distribution.png`: Visualization of data distribution
- `NLP PROJECT.ipynb`: Jupyter notebook with model training code

## Requirements

The application uses the following Python libraries:
- streamlit
- joblib
- nltk
- re (built-in)
- sklearn (for TF-IDF)

## How to Run

1. Install requirements: `pip install streamlit joblib nltk scikit-learn`
2. Download the required NLTK data: `python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"`
3. Run the app: `streamlit run app.py`

## Usage

1. Enter a mobile phone review in the text area
2. Click "Analyze Sentiment" button
3. View the predicted sentiment (Positive/Negative)