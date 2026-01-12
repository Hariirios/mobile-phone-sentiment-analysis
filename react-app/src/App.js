import React, { useState } from 'react';
import { analyzeSentiment } from './services/api';
import './App.css';

function App() {
  const [review, setReview] = useState('');
  const [sentiment, setSentiment] = useState(null);
  const [confidence, setConfidence] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSentimentAnalysis = async () => {
    if (!review.trim()) {
      alert('Please enter a review');
      return;
    }

    setLoading(true);
    
    try {
      // In a real implementation, uncomment the following lines and connect to your backend API
      /*
      const result = await analyzeSentiment(review);
      setSentiment(result.sentiment);
      setConfidence(result.confidence);
      */
      
      // Simulating API call to backend (in a real app, this would call your ML model)
      // For now, we'll simulate the response
      setTimeout(() => {
        // Simple heuristic for demo purposes - in a real app, this would come from your ML model
        const positiveWords = ['good', 'great', 'excellent', 'amazing', 'love', 'perfect', 'awesome', 'fantastic', 'brilliant', 'outstanding'];
        const negativeWords = ['bad', 'terrible', 'awful', 'horrible', 'hate', 'worst', 'disappointing', 'poor', 'useless', 'broken'];
        
        const reviewLower = review.toLowerCase();
        let positiveCount = 0;
        let negativeCount = 0;
        
        positiveWords.forEach(word => {
          if (reviewLower.includes(word)) positiveCount++;
        });
        
        negativeWords.forEach(word => {
          if (reviewLower.includes(word)) negativeCount++;
        });
        
        let predictedSentiment = 'neutral';
        let conf = 0.5;
        
        if (positiveCount > negativeCount) {
          predictedSentiment = 'positive';
          conf = Math.min(0.95, 0.5 + (positiveCount * 0.1));
        } else if (negativeCount > positiveCount) {
          predictedSentiment = 'negative';
          conf = Math.min(0.95, 0.5 + (negativeCount * 0.1));
        }
        
        setSentiment(predictedSentiment);
        setConfidence(conf.toFixed(2));
        setLoading(false);
      }, 1500); // Simulate processing time
    } catch (error) {
      console.error('Error analyzing sentiment:', error);
      alert('Error analyzing sentiment. Please try again.');
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    handleSentimentAnalysis();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-blue-900 text-white">
      {/* Animated background elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
        <div className="absolute top-1/3 right-1/4 w-64 h-64 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute bottom-1/4 left-1/2 w-64 h-64 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      <div className="relative z-10 container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl md:text-6xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
            📱 Mobile Phone Review Sentiment Analysis
          </h1>
          <p className="text-lg text-blue-200 max-w-2xl mx-auto">
            Discover the sentiment behind customer reviews with our AI-powered analysis
          </p>
        </header>

        <main className="max-w-4xl mx-auto">
          <div className="bg-gray-800/50 backdrop-blur-lg rounded-2xl p-6 md:p-8 shadow-2xl border border-gray-700">
            <form onSubmit={handleSubmit}>
              <div className="mb-6">
                <label htmlFor="review" className="block text-lg font-medium mb-3">
                  Enter Mobile Phone Review
                </label>
                <textarea
                  id="review"
                  value={review}
                  onChange={(e) => setReview(e.target.value)}
                  rows="6"
                  className="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white placeholder-gray-400 resize-none"
                  placeholder="I really love this phone! The camera quality is amazing and battery life is great..."
                ></textarea>
              </div>

              <button
                type="submit"
                disabled={loading}
                className={`w-full py-4 px-6 rounded-xl font-bold text-lg transition-all duration-300 ${
                  loading 
                    ? 'bg-gray-600 cursor-not-allowed' 
                    : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transform hover:scale-[1.02] shadow-lg hover:shadow-blue-500/30'
                }`}
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Analyzing...
                  </span>
                ) : (
                  '🔍 Analyze Sentiment'
                )}
              </button>
            </form>

            {sentiment && !loading && (
              <div className="mt-8 p-6 bg-gradient-to-br from-gray-700/50 to-gray-800/50 rounded-xl border border-gray-600 shadow-lg">
                <h2 className="text-xl font-semibold mb-4 text-center">Analysis Results</h2>
                
                <div className={`text-3xl font-bold text-center mb-4 ${
                  sentiment === 'positive' ? 'text-green-400' : 'text-red-400'
                }`}>
                  {sentiment === 'positive' ? '✅ POSITIVE' : '❌ NEGATIVE'}
                </div>
                
                <div className="text-center text-lg">
                  <p>Confidence: <span className="font-semibold">{confidence * 100}%</span></p>
                </div>
                
                <div className="mt-4 text-center text-sm text-gray-300">
                  <p>Note: This is simulated analysis. In a real implementation, this would connect to your ML model.</p>
                </div>
              </div>
            )}

            {!sentiment && !loading && (
              <div className="mt-8 p-6 bg-gray-700/30 rounded-xl border border-gray-600 text-center text-gray-300">
                <p>Your sentiment analysis results will appear here</p>
              </div>
            )}
          </div>

          <div className="mt-10 bg-gray-800/30 backdrop-blur-sm rounded-2xl p-6 border border-gray-700">
            <h2 className="text-xl font-semibold mb-4 text-center text-blue-300">How It Works</h2>
            <ul className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <li className="bg-gray-700/50 p-4 rounded-lg border border-gray-600">
                <div className="text-blue-400 text-2xl mb-2">1</div>
                <h3 className="font-medium mb-1">Input Review</h3>
                <p className="text-sm text-gray-300">Enter a mobile phone review in the text area</p>
              </li>
              <li className="bg-gray-700/50 p-4 rounded-lg border border-gray-600">
                <div className="text-purple-400 text-2xl mb-2">2</div>
                <h3 className="font-medium mb-1">AI Analysis</h3>
                <p className="text-sm text-gray-300">Our ML model analyzes the sentiment</p>
              </li>
              <li className="bg-gray-700/50 p-4 rounded-lg border border-gray-600">
                <div className="text-pink-400 text-2xl mb-2">3</div>
                <h3 className="font-medium mb-1">Get Results</h3>
                <p className="text-sm text-gray-300">Receive sentiment classification with confidence</p>
              </li>
            </ul>
          </div>
        </main>

        <footer className="mt-16 text-center text-gray-400">
          <p>Built using React and Tailwind CSS</p>
        </footer>
      </div>

      <style jsx>{`
        @keyframes blob {
          0% {
            transform: translate(0px, 0px) scale(1);
          }
          33% {
            transform: translate(30px, -50px) scale(1.1);
          }
          66% {
            transform: translate(-20px, 20px) scale(0.9);
          }
          100% {
            transform: translate(0px, 0px) scale(1);
          }
        }
        
        .animate-blob {
          animation: blob 7s infinite;
        }
        
        .animation-delay-2000 {
          animation-delay: 2s;
        }
        
        .animation-delay-4000 {
          animation-delay: 4s;
        }
      `}</style>
    </div>
  );
}

export default App;