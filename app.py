import streamlit as st
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Load model and vectorizer
tfidf = joblib.load('tfidf_vectorizer.pkl')
model = joblib.load('sentiment_model.pkl')



# Download required NLTK data for Streamlit Cloud
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


# NLP tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return ' '.join(tokens)

# App UI
st.title("Mobile Phone Review Sentiment Analysis")

review = st.text_area("Enter a customer review")

if st.button("Analyze Sentiment"):
    cleaned = preprocess_text(review)
    vectorized = tfidf.transform([cleaned])
    prediction = model.predict(vectorized)[0]
    st.success(f"Predicted Sentiment: {prediction.capitalize()}")
