const axios = require('axios');

async function fetchBTCCloses(limit = 100) {
  const url = `https://finnhub.io/api/v1/crypto/candle?symbol=BINANCE:BTCUSDT&resolution=1&count=${limit}&token=${process.env.FINNHUB_KEY}`;
  try {
    const response = await axios.get(url);
    return response.data.c.reverse();
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

  if (rsi <= 30 && price < vwap) {
    await channel.send(`🎯 **Sniper Setup Detected**
• RSI: ${rsi}
• Price: $${price}
• VWAP: $${vwap}
> RSI < 30 + price under VWAP — possible trap.`);
  } else {
    await channel.send(`📉 RSI: ${rsi} | Price: $${price} | VWAP: $${vwap} — no sniper setup yet.\nGPT: scan again in 60s`);
  }
}

async function handleCustomMessage(message) {
  const content = message.content.toLowerCase();

  if (content.includes('what') && content.includes('going on')) {
    await message.reply('🧠 Scanning latest sniper signals... hold tight.');
    await checkSniperConditions(message.channel);
  }

  else if (content.includes('scan again')) {
    await message.reply('🔁 Rechecking RSI/VWAP confluence...');
    await checkSniperConditions(message.channel);
  }

  else if (content.includes('override')) {
    await message.reply('⚠️ Manual override: forcing sniper scan...');
    await checkSniperConditions(message.channel);
  }

  else if (content.includes('rsi') || content.includes('vwap')) {
    const closes = await fetchBTCCloses();
    const rsi = calculateRSI(closes);
    const price = closes[closes.length - 1];
    const vwap = calculateVWAP(closes.slice(-20));
    await message.reply(`🧾 **Market Stats**
• RSI: ${rsi}
• Price: $${price}
• VWAP: $${vwap}`);
  }

  else {
    await message.reply('🤖 Command not recognized. Try: `GPT: what’s going on?`, `GPT: scan again`, or `GPT: RSI VWAP now`');
  }
}

module.exports = {
  checkSniperConditions,
  handleCustomMessage
};
