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
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0").strip())

# Set up Discord bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# MEXC orderbook fetcher
def get_mexc_orderbook(symbol="BTC_USDT", limit=20):
    url = f"https://api.mexc.com/api/v3/depth?symbol={symbol}&limit={limit}"
    response = requests.get(url)
    return response.json()

# Simple trap signal analyzer
def analyze_orderbook(data):
    bids = data.get("bids", [])
    asks = data.get("asks", [])
    if not bids or not asks:
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
        print("❌ Channel not found. Check DISCORD_CHANNEL_ID.")

# On ready event
@bot.event
async def on_ready():
    print(f"✅ Discord bot connected as {bot.user}")
    while True:
        try:
            data = get_mexc_orderbook()
            analysis = analyze_orderbook(data)

            if analysis:
                msg = (
                    f"📊 **BTC/USDT Sniper Watch**\n"
                    f"Price: **{analysis['price']}**\n"
                    f"💚 Max Bid: {analysis['max_bid'][1]} @ {analysis['max_bid'][0]}\n"
                    f"❤️ Max Ask: {analysis['max_ask'][1]} @ {analysis['max_ask'][0]}"
                )
                print(msg)
                await send_discord_alert(msg)
            else:
                print("⚠️ Orderbook data empty or invalid")

            await asyncio.sleep(60)

        except Exception as e:
            print(f"❌ Error: {e}")
            await asyncio.sleep(15)

# Run bot
if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
