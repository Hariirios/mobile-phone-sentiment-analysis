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
st.set_page_config(page_title="Mobile Phone Sentiment Analyzer", page_icon="📱", layout="wide")

# Custom CSS styling with dark futuristic background
css = """
<style>
/* Dark futuristic background */
[data-testid="stAppViewContainer"] > .main {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    min-height: 100vh;
    position: relative;
}

@keyframes gradientBG {
    0% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
}

/* Content container */
[data-testid="stAppViewContainer"] > .main > div {
    background-color: rgba(15, 25, 40, 0.85);
    backdrop-filter: blur(10px);
    min-height: 100vh;
    padding: 20px;
}

/* Card styling */
.card {
    background: rgba(30, 40, 60, 0.9);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(100, 150, 255, 0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
}

/* Text area styling */
.stTextArea > label {
    font-size: 18px;
    font-weight: bold;
    color: #e0e0ff;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(45deg, #6a11cb, #2575fc);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 15px 30px;
    font-size: 18px;
    font-weight: bold;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    background: linear-gradient(45deg, #2575fc, #6a11cb);
}

/* Result container */
.result-container {
    background: rgba(40, 50, 70, 0.9);
    padding: 30px;
    border-radius: 15px;
    margin-top: 20px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    border-left: 5px solid #6a11cb;
}

/* Header */
.header {
    text-align: center;
    margin-bottom: 40px;
}

.header h1 {
    font-size: 3rem;
    color: #ffffff;
    margin-bottom: 10px;
    background: linear-gradient(45deg, #6a11cb, #2575fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-fill-color: transparent;
}

.header p {
    font-size: 1.3rem;
    color: #a0d2ff;
    max-width: 600px;
    margin: 0 auto;
}

/* Sentiment styles */
.positive {
    color: #2ecc71;
    font-weight: bold;
    font-size: 28px;
    text-align: center;
}

.negative {
    color: #e74c3c;
    font-weight: bold;
    font-size: 28px;
    text-align: center;
}

/* Info box */
.info-box {
    background: rgba(35, 45, 65, 0.8);
    padding: 20px;
    border-radius: 12px;
    margin: 20px 0;
    border-left: 4px solid #3498db;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

/* Footer */
footer {
    text-align: center;
    color: #a0d2ff;
    margin-top: 40px;
    padding: 30px;
    font-size: 1.1rem;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# Header
st.markdown('<div class="header"><h1>📱 Mobile Phone Review Sentiment Analysis</h1><p>Discover the sentiment behind customer reviews</p></div>', unsafe_allow_html=True)

# Main content layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📝 Enter Review")
    review = st.text_area("Type your mobile phone review here:", height=200, placeholder="I really love this phone! The camera quality is amazing and battery life is great...")
    
    analyze_button = st.button("🔍 Analyze Sentiment", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Result")
    if analyze_button:
        if review.strip():
            with st.spinner('Analyzing sentiment...'):
                cleaned = preprocess_text(review)
                vectorized = tfidf.transform([cleaned])
                prediction = model.predict(vectorized)[0]
                confidence = model.predict_proba(vectorized)[0].max()  # Get confidence score if available
                
                # Display result with appropriate styling
                if prediction.lower() == 'positive':
                    st.markdown(f'<div class="result-container"><p>Your review sentiment is:</p><p class="positive">✅ POSITIVE</p><p style="text-align: center;">Confidence: {confidence:.2f}</p></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="result-container"><p>Your review sentiment is:</p><p class="negative">❌ NEGATIVE</p><p style="text-align: center;">Confidence: {confidence:.2f}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box">Please enter a review to analyze.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box">Click the button to analyze the sentiment of your review.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Additional info
st.markdown('<div class="info-box" style="margin-top: 30px;"><p><strong>Tip:</strong> Enter a review about a mobile phone to analyze whether the sentiment is positive or negative. Our ML model will classify the sentiment based on the text you provide.</p></div>', unsafe_allow_html=True)

# Add footer
st.markdown("---")
st.markdown("<footer>Built with ❤️ using Streamlit and Machine Learning</footer>", unsafe_allow_html=True)
