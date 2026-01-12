// Backend server to serve the ML model
// This is a template for how you would connect your Python ML model to the React frontend

const express = require('express');
const cors = require('cors');
const path = require('path');
const { spawn } = require('child_process');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.static('build')); // Serve built React app in production

// Raw body parser for analyze endpoint to completely bypass JSON parsing issues
app.use('/analyze', express.raw({ type: 'application/json', inflate: true, limit: '10mb' }));

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Endpoint to analyze sentiment
app.post('/analyze', async (req, res) => {
  console.log('Analyze endpoint hit');
  console.log('Request body:', req.body);
  console.log('Request headers:', req.headers['content-type']);
  
  try {
    // Parse the raw buffer body as JSON
    let parsedBody;
    try {
      parsedBody = JSON.parse(req.body.toString());
    } catch (parseError) {
      console.error('Error parsing JSON:', parseError);
      return res.status(400).json({ error: 'Invalid JSON format' });
    }
    const { text } = parsedBody;

    console.log('Extracted text:', text);
    
    if (!text) {
      console.log('No text provided');
      return res.status(400).json({ error: 'Text is required' });
    }

    // Log the request for debugging
    console.log('Received analyze request with text:', text);
    
    // In a real implementation, you would call your Python ML model here
    // This is a simplified example using a Python subprocess
    const pythonProcess = spawn('python', ['./predict_sentiment.py', text], {
      cwd: __dirname, // Execute from the current directory (react-app)
      stdio: ['pipe', 'pipe', 'pipe']
    });
    
    // Log the command being executed
    console.log('Executing Python command: python ./predict_sentiment.py', text);
    
    // Flag to track if response has been sent
    let responseSent = false;
    let stderrData = '';
    
    pythonProcess.stdout.on('data', (data) => {
      console.log('Python stdout:', data.toString());
      if (!responseSent) {
        try {
          const result = JSON.parse(data.toString());
          console.log('Parsed result:', result);
          responseSent = true;
          res.json({
            sentiment: result.sentiment,
            confidence: result.confidence
          });
        } catch (parseError) {
          console.error('Error parsing Python output:', parseError);
          console.error('Raw output:', data.toString());
          if (!responseSent) {
            responseSent = true;
            res.status(500).json({ error: 'Error processing sentiment analysis' });
          }
        }
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      stderrData += data.toString();
      console.error('Python stderr:', data.toString());
    });
    
    pythonProcess.on('close', (code) => {
      console.log('Python process closed with code:', code);
      if (!responseSent) {
        if (code !== 0) {
          responseSent = true;
          res.status(500).json({ error: `Python process exited with code ${code}. Error: ${stderrData}` });
        } else {
          // If process exits with code 0 but no data was received, return error
          if (!stderrData && !responseSent) {
            responseSent = true;
            res.status(500).json({ error: 'No response from Python script' });
          }
        }
      }
    });

  } catch (error) {
    console.error('Server error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Serve React app in production
app.get(/^(?!\/health|\/analyze).*$/, (req, res) => {
  res.sendFile(path.join(__dirname, 'build/index.html'));
});

// Global error handler
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({ error: 'Internal server error' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
  console.log(`API endpoint: http://localhost:${PORT}/analyze`);
});