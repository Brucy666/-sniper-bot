// index.js
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// Home route (just to test if bot is live)
app.get('/', (req, res) => {
  res.send('✅ GPT Sniper Terminal is Running');
});

// Webhook route (this is where TradingView or other services will send alerts)
app.post('/webhook', (req, res) => {
  console.log('🚀 Received webhook:', req.body);
  res.status(200).send('Received');
});

app.listen(PORT, () => {
  console.log(`✅ GPT Sniper Terminal is Live on port ${PORT}`);
});
