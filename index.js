require('dotenv').config();
const { Client, GatewayIntentBits } = require('discord.js');
const checkSniperConditions = require('./sniper_logic_agent');

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

client.once('ready', () => {
  console.log(`⚙️ GPT Sniper Terminal is live as ${client.user.tag}`);

  const terminal = client.channels.cache.find(c => c.name === 'gpt-terminal');

  if (!terminal) {
    console.log('⚠️ Could not find #gpt-terminal channel!');
    return;
  }

  // 🔁 Initial trigger
  checkSniperConditions(terminal);
});

// 🔁 Self-triggering loop based on bot’s own message
client.on("messageCreate", (message) => {
  if (
    message.author.bot &&
    message.content.includes("GPT: scan again in")
  ) {
    const terminal = message.channel;
    setTimeout(() => {
      checkSniperConditions(terminal);
    }, 60000); // 60 seconds
  }
});

client.login(process.env.TOKEN);
