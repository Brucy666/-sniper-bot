// index.js
import express from 'express';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.send('✅ GPT Sniper Terminal is Running');
});

app.post('/webhook', (req, res) => {
  console.log('🚀 Received webhook:', req.body);
  res.status(200).send('Received');
});

app.listen(PORT, () => {
  console.log(`✅ GPT Sniper Terminal is Live on port ${PORT}`);
});
