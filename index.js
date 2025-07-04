require('dotenv').config();
const { Client, GatewayIntentBits } = require('discord.js');
const { checkSniperConditions, handleCustomMessage } = require('./sniper_logic_agent');

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

client.once('ready', () => {
  console.log(`🚀 GPT Sniper Terminal is Live as ${client.user.tag}`);
});

client.on('messageCreate', async (message) => {
  if (message.author.bot) return;

  const content = message.content.toLowerCase();
  if (content.startsWith('gpt:')) {
    await handleCustomMessage(message);
  }
});

client.login(process.env.TOKEN);
