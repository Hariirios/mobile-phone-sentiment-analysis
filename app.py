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
st.set_page_config(page_title="Mobile Phone Sentiment Analyzer", page_icon="📱", layout="wide")

# Custom CSS styling with dark futuristic background
css = """
<style>
/* Modern glassmorphism design inspired by Pinterest/Figma */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Background with subtle animated gradient */
[data-testid="stAppViewContainer"] > .main {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    min-height: 100vh;
    position: relative;
    font-family: 'Inter', sans-serif;
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
    background-color: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(10px);
    min-height: 100vh;
    padding: 20px;
}

/* Modern card styling with glass effect */
.card {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 35px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), transform 0.3s ease;
    margin-bottom: 25px;
}

.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(255, 255, 255, 0.4);
}

/* Text area styling with modern look */
.stTextArea > label {
    font-size: 18px;
    font-weight: 600;
    color: #2c3e50;
    font-family: 'Inter', sans-serif;
}

.stTextArea textarea {
    border-radius: 15px !important;
    border: 1px solid #e0e6ed !important;
    padding: 15px !important;
    font-family: 'Inter', sans-serif;
    font-size: 16px;
    transition: all 0.3s ease;
}

.stTextArea textarea:focus {
    border: 1px solid #3498db !important;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2) !important;
}

/* Button styling with modern gradient */
.stButton > button {
    background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
    color: white;
    border: none;
    border-radius: 16px;
    padding: 16px 32px;
    font-size: 18px;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.5px;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 4px 20px rgba(106, 17, 203, 0.3);
    width: 100%;
}

.stButton > button:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(106, 17, 203, 0.4);
    background: linear-gradient(135deg, #2575fc 0%, #6a11cb 100%);
}

.stButton > button:active {
    transform: translateY(0);
}

/* Result container with enhanced styling */
.result-container {
    background: rgba(255, 255, 255, 0.9);
    padding: 30px;
    border-radius: 20px;
    margin-top: 25px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08), 0 0 0 1px rgba(255, 255, 255, 0.5);
    border-left: 6px solid #3498db;
    text-align: center;
}

/* Header with modern typography */
.header {
    text-align: center;
    margin-bottom: 45px;
    padding: 0 20px;
}

.header h1 {
    font-size: 2.8rem;
    color: #2c3e50;
    margin-bottom: 12px;
    font-weight: 700;
    font-family: 'Inter', sans-serif;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #6a11cb, #2575fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-fill-color: transparent;
}

.header p {
    font-size: 1.2rem;
    color: #7f8c8d;
    max-width: 650px;
    margin: 0 auto;
    font-family: 'Inter', sans-serif;
    font-weight: 400;
    line-height: 1.6;
}

/* Sentiment styles with enhanced visuals */
.positive {
    color: #27ae60;
    font-weight: 700;
    font-size: 32px;
    text-align: center;
    font-family: 'Inter', sans-serif;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 15px 0;
    text-shadow: 0 2px 4px rgba(39, 174, 96, 0.2);
}

.negative {
    color: #e74c3c;
    font-weight: 700;
    font-size: 32px;
    text-align: center;
    font-family: 'Inter', sans-serif;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 15px 0;
    text-shadow: 0 2px 4px rgba(231, 76, 60, 0.2);
}

.confidence-score {
    font-size: 18px;
    color: #7f8c8d;
    font-weight: 500;
    margin-top: 15px;
    font-family: 'Inter', sans-serif;
}

/* Info box with modern styling */
.info-box {
    background: rgba(236, 240, 241, 0.8);
    padding: 25px;
    border-radius: 18px;
    margin: 25px 0;
    border-left: 5px solid #3498db;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
    font-family: 'Inter', sans-serif;
}

.info-box strong {
    color: #2c3e50;
}

/* Footer with elegant styling */
footer {
    text-align: center;
    color: #7f8c8d;
    margin-top: 45px;
    padding: 35px;
    font-size: 1rem;
    font-family: 'Inter', sans-serif;
    font-weight: 400;
}

/* Spinner styling */
div.stSpinner > div > div {
    background: linear-gradient(135deg, #6a11cb, #2575fc) !important;
}

/* Column gap adjustment */
[data-testid="stHorizontalBlock"] {
    gap: 2rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .header h1 {
        font-size: 2.2rem;
    }
    
    .header p {
        font-size: 1rem;
    }
    
    .card {
        padding: 25px;
    }
    
    .result-container {
        padding: 25px;
    }
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
                    st.markdown(f'<div class="result-container"><p style="font-size: 20px; font-weight: 600; margin-bottom: 15px; color: #2c3e50;">Your review sentiment is:</p><p class="positive">✅ POSITIVE</p><p class="confidence-score">Confidence: {confidence:.2f}</p></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="result-container"><p style="font-size: 20px; font-weight: 600; margin-bottom: 15px; color: #2c3e50;">Your review sentiment is:</p><p class="negative">❌ NEGATIVE</p><p class="confidence-score">Confidence: {confidence:.2f}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box">Please enter a review to analyze.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box">Click the button to analyze the sentiment of your review.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Additional info
st.markdown('<div class="info-box" style="margin-top: 30px;"><p><strong>💡 Tip:</strong> Enter a review about a mobile phone to analyze whether the sentiment is positive or negative. Our ML model will classify the sentiment based on the text you provide.</p></div>', unsafe_allow_html=True)

# Add footer
st.markdown("---")
st.markdown("<footer>Built using Streamlit and Machine Learning</footer>", unsafe_allow_html=True)
