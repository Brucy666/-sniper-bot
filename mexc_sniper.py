import os
import time
import asyncio
import requests
import discord
from discord.ext import commands

# Load environment variables
MEXC_API_KEY = os.getenv("MEXC_API_KEY")
MEXC_API_SECRET = os.getenv("MEXC_API_SECRET")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN") or os.getenv("TOKEN")
DISCORD_CHANNEL_ID = int("".join(filter(str.isdigit, os.getenv("DISCORD_CHANNEL_ID", ""))))

# Discord bot setup with message content intent
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Fetch orderbook from MEXC
def get_mexc_orderbook(symbol="BTCUSDT", limit=20):
    url = f"https://api.mexc.com/api/v3/depth?symbol={symbol}&limit={limit}"
    print(f"🔗 Fetching: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"❌ Error fetching orderbook: {e}")
        return None

# Analyze orderbook for sniper setup
def analyze_orderbook(data):
    if not data or "bids" not in data or "asks" not in data:
        print("⚠️ Invalid or empty orderbook:", data)
        return None

    bids = data["bids"]
    asks = data["asks"]
    if not bids or not asks:
        print("⚠️ No bids or asks found.")
        return None

    max_bid = max(bids, key=lambda x: float(x[1]))
    max_ask = max(asks, key=lambda x: float(x[1]))
    price = (float(bids[0][0]) + float(asks[0][0])) / 2

    return {
        "price": round(price, 2),
        "max_bid": max_bid,
        "max_ask": max_ask
    }

# Send alert to Discord
async def send_discord_alert(message):
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(message)
    else:
        print("❌ Channel not found.")

# Listen for GPT prompts
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("GPT:"):
        prompt = message.content.replace("GPT:", "").strip()
        print(f"🧠 Received GPT prompt: {prompt}")
        reply = f"🤖 Received: `{prompt}` — reply will be handled in terminal soon."
        await message.channel.send(reply)

    await bot.process_commands(message)

# On bot ready, start sniper loop
@bot.event
async def on_ready():
    print(f"✅ Discord bot connected as {bot.user}")
    while True:
        try:
            data = get_mexc_orderbook()
            print("📥 Raw data:", data)

            analysis = analyze_orderbook(data)
            if analysis:
                msg = (
                    f"📊 **BTC/USDT Sniper Watch**\n"
                    f"Price: **{analysis['price']}**\n"
                    f"💚 Max Bid: {analysis['max_bid'][1]} @ {analysis['max_bid'][0]}\n"
                    f"❤️ Max Ask: {analysis['max_ask'][1]} @ {analysis['max_ask'][0]}"
                )
                print("📤 Posting to Discord...")
                await send_discord_alert(msg)

            await asyncio.sleep(60)

        except Exception as e:
            print(f"❌ Runtime error: {e}")
            await asyncio.sleep(15)

# Run the bot
if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
