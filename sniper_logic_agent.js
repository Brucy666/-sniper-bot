const axios = require("axios");
const url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=1&interval=minutely";

async function fetchBTCCloses(limit = 100) {
  try {
    const response = await axios.get(url);
    return response.data.prices.map(c => parseFloat(c[1])).reverse();
  } catch (error) {
    console.error("❌ Error fetching BTC data:", error.message);
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
  const price = closes[0]; // most recent
  const vwap = calculateVWAP(closes.slice(0, 20)); // 20-minute window

  if (rsi && rsi < 30 && price < vwap) {
    await channel.send(
      `🎯 **Sniper Setup Detected**\nRSI: ${rsi} | Price: $${price} | VWAP: $${vwap}\n↳ RSI < 30 + price under VWAP = possible trap.`
    );
  } else {
    await channel.send(
      `📉 RSI: ${rsi} | Price: $${price} | VWAP: $${vwap} — no sniper setup yet.`
    );
  }

  // 🔁 Self-prompt for continuation
  channel.send("GPT: scan again in 60s");
}

module.exports = { checkSniperConditions };
