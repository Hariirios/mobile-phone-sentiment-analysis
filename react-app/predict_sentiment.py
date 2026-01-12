"""
Python script to interface with the ML model for sentiment analysis
This script is called by the Node.js backend to perform predictions
"""

import sys
import json
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

def preprocess_text(text):
    """Preprocess the input text for the model"""
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    
    # Initialize stopwords and lemmatizer (assuming they're available)
    try:
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    except LookupError:
        # Fallback if NLTK data is not available
        tokens = [word for word in tokens]
    
    return ' '.join(tokens)

def load_models():
    """Load the trained models"""
    try:
        # Adjust paths as needed based on where the models are stored
        tfidf = joblib.load('../tfidf_vectorizer.pkl')
        model = joblib.load('../sentiment_model.pkl')
        return tfidf, model
    except FileNotFoundError:
        print(json.dumps({"error": "Model files not found"}))
        sys.exit(1)

def predict_sentiment(text):
    """Predict the sentiment of the given text"""
    # Load models
    tfidf, model = load_models()
    
    # Preprocess the text
    cleaned_text = preprocess_text(text)
    
    # Transform the text using the TF-IDF vectorizer
    vectorized = tfidf.transform([cleaned_text])
    
    # Predict the sentiment
    prediction = model.predict(vectorized)[0]
    
    # Get prediction probability if available
    try:
        confidence = model.predict_proba(vectorized)[0].max()
    except AttributeError:
        # If predict_proba is not available, set a default confidence
        confidence = 0.8
    
    return {
        "sentiment": prediction,
        "confidence": float(confidence)
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Text input is required"}))
        sys.exit(1)
    
    # Get text from command line argument
    input_text = ' '.join(sys.argv[1:])
    
    try:
        result = predict_sentiment(input_text)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)