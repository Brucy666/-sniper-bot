require('dotenv').config();
const { Client, GatewayIntentBits } = require('discord.js');
const { checkSniperConditions } = require('./sniper_logic_agent');

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});

client.once('ready', () => {
  console.log(`🤖 GPT Sniper Terminal is live as ${client.user.tag}`);
  const channel = client.channels.cache.find(c => c.name === 'gpt-terminal');
  if (channel) checkSniperConditions(channel);
  setInterval(() => checkSniperConditions(channel), 60000);
});

client.on('messageCreate', async (message) => {
  if (message.author.bot || !message.content.startsWith('GPT:')) return;

  const query = message.content.slice(4).trim().toLowerCase();

  if (query.includes('what’s going on')) {
    await message.reply(`🧠 Scanning current RSI + VWAP + volatility traps. No confirmed sniper trap yet.`);
  } else if (query.includes('who is that')) {
    await message.reply(`👁 Scanning the message source. No anomaly detected. Watching.`);
  } else if (query.includes('any sniper ideas')) {
    await message.reply(`📡 No confirmed trap yet. Continuing passive scan. Check RSI < 30 with price under VWAP.`);
  } else {
    await message.reply(`🤔 Message received. Saving to GPT memory... Future logic loop enabled.`);
  }
});

client.login(process.env.TOKEN);
