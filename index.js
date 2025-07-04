// index.js
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// Default route
app.get('/', (req, res) => {
  res.send('GPT Sniper Terminal is Running');
});

// Example webhook endpoint
app.post('/webhook', (req, res) => {
  console.log('Received webhook:', req.body);
  res.sendStatus(200);
});

app.listen(PORT, () => {
  console.log(`✅ GPT Sniper Terminal is Live on port ${PORT}`);
});
