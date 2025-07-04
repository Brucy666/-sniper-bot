require('dotenv').config();
const { Client, GatewayIntentBits } = require('discord.js');
const { checkSniperConditions } = require('./sniper_logic_agent');

const memory = [];

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});

client.once('ready', async () => {
  console.log(`🧠 GPT Sniper Terminal is live as ${client.user.tag}`);
  const channel = client.channels.cache.find(c => c.name === 'gpt-terminal');
  if (!channel) return;

  await checkSniperConditions(channel, memory); // first scan
  setInterval(() => checkSniperConditions(channel, memory), 60000);
});

client.on('messageCreate', async (message) => {
  if (message.author.bot || !message.content.startsWith('GPT:')) return;

  const query = message.content.slice(4).trim().toLowerCase();

  if (query.includes("what’s going on")) {
    await message.reply("🧠 I’m scanning RSI + VWAP. Monitoring for traps...");
  } else if (query.includes("who is that")) {
    await message.reply("🔍 Observing the message source... no anomaly yet.");
  } else if (query.includes("any sniper ideas")) {
    await message.reply("🧠 Nothing clean yet. Waiting for RSI + VWAP to align.");
  } else {
    await message.reply("📓 Message received. Memory updated.");
    memory.push({ from: 'user', content: query, time: Date.now() });
  }
});

client.login(process.env.TOKEN);
