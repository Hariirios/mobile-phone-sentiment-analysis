# Mobile Phone Sentiment Analysis React App

A React application for analyzing the sentiment of mobile phone reviews using Tailwind CSS for styling.

## Features

- Beautiful, modern UI with animated background
- Responsive design that works on all devices
- Simulated sentiment analysis (connects to your ML model in production)
- Clean, intuitive user interface

## Installation

1. Make sure you have Node.js installed on your system
2. Navigate to this directory: `cd react-app`
3. Install dependencies: `npm install`
4. Start the development server: `npm start`

## Connecting to Your ML Model

The current implementation simulates sentiment analysis. To connect to your actual ML model:

1. Set up a backend API endpoint that accepts text and returns sentiment
2. Replace the simulation logic in `App.js` with an API call to your model
3. Ensure CORS is configured if your backend runs on a different port

Example API integration:
```javascript
const analyzeSentiment = async () => {
  // Replace with your actual API endpoint
  const response = await fetch('/api/analyze-sentiment', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ review }),
  });
  
  const data = await response.json();
  setSentiment(data.sentiment);
  setConfidence(data.confidence);
};
```

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.