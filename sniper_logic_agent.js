require('dotenv').config();
const axios = require('axios');

const FINNHUB_KEY = process.env.FINNHUB_KEY;
const url = `https://finnhub.io/api/v1/crypto/candle?symbol=BINANCE:BTCUSDT&resolution=1&count=100&token=${FINNHUB_KEY}`;

async function fetchBTCCloses() {
  try {
    const response = await axios.get(url);
    return response.data.c.map(c => parseFloat(c)).reverse();
  } catch (error) {
    console.error('❌ Error fetching BTC data:', error.message);
    return [];
  }
}

function calculateRSI(closes, period = 14) {
  if (closes.length < period + 1) return null;

  let gains = 0, losses = 0;
  for (let i = 1; i <= period; i++) {
    const delta = closes[i] - closes[i - 1];
    if (delta >= 0) gains += delta;
    else losses -= delta;
  }

  const avgGain = gains / period;
  const avgLoss = losses / period;
  if (avgLoss === 0) return 100;

  const rs = avgGain / avgLoss;
  return Math.round(100 - 100 / (1 + rs));
}

function calculateVWAP(closes) {
  const sum = closes.reduce((acc, val) => acc + val, 0);
  return parseFloat((sum / closes.length).toFixed(2));
}

async function checkSniperConditions(channel) {
  const closes = await fetchBTCCloses();
  if (!closes.length) return;

  const rsi = calculateRSI(closes);
  const price = closes[closes.length - 1];
  const vwap = calculateVWAP(closes.slice(-20));

  if (rsi && rsi <= 30 && price < vwap) {
    await channel.send(`🎯 **Sniper Setup Detected**\nRSI: ${rsi} | Price: $${price} | VWAP: $${vwap}\n🔻 RSI < 30 + price under VWAP — possible trap.`);
  } else {
    await channel.send(`📉 RSI: ${rsi} | Price: $${price} | VWAP: $${vwap} — no sniper setup yet.`);
  }

  await channel.send("GPT: scan again in 60s");
}

module.exports = { checkSniperConditions };
