#!/bin/bash
# Setup script for Heroku deployment

# Install Python dependencies
pip install -r requirements.txt

# Install NLTK data (needed for the sentiment analysis)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"