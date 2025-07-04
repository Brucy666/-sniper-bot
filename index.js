require('dotenv').config();
const { Client, GatewayIntentBits } = require('discord.js');
const { checkSniperConditions } = require('./sniper_logic_agent');

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

client.once('ready', () => {
  console.log(`✅ GPT Sniper Terminal is live as ${client.user.tag}`);

  const terminal = client.channels.cache.find(c => c.name === 'gpt-terminal');
  setInterval(() => {
    if (terminal) {
      checkSniperConditions(terminal);
    } else {
      console.log('⚠️ Could not find #gpt-terminal channel!');
    }
  }, 60000); // every 60s
});

client.login(process.env.TOKEN);
