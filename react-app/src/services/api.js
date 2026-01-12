// API service to connect to your ML model
// This is a template - you'll need to implement your backend to serve your model

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

/**
 * Analyzes the sentiment of a given text
 * @param {string} text - The text to analyze
 * @returns {Promise<{sentiment: string, confidence: number}>} The analysis result
 */
export const analyzeSentiment = async (text) => {
  try {
    // In a real implementation, this would be an API call to your backend
    // that connects to your trained model
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error analyzing sentiment:', error);
    throw error;
  }
};

/**
 * Gets health status of the API
 * @returns {Promise<boolean>} Whether the API is healthy
 */
export const checkHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.ok;
  } catch (error) {
    console.error('Error checking API health:', error);
    return false;
  }
};