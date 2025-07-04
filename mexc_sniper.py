import os
import time
import requests
import discord
from discord.ext import commands

# ENV VARS
MEXC_API_KEY = os.getenv("MEXC_API_KEY")
MEXC_API_SECRET = os.getenv("MEXC_API_SECRET")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN") or os.getenv("TOKEN")  # fallback if named TOKEN
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0"))

# Discord client
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def get_mexc_orderbook(symbol="BTC_USDT", limit=20):
    url = f"https://api.mexc.com/api/v3/depth?symbol={symbol}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    return data

def analyze_orderbook(data):
    bids = data["bids"]
    asks = data["asks"]
    max_bid = max(bids, key=lambda x: float(x[1]))
    max_ask = max(asks, key=lambda x: float(x[1]))
    price = (float(bids[0][0]) + float(asks[0][0])) / 2
    return {
        "price": round(price, 2),
        "max_bid": max_bid,
        "max_ask": max_ask
    }

async def send_discord_alert(message):
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(message)
    else:
        print("❌ Channel not found. Check DISCORD_CHANNEL_ID.")

@bot.event
async def on_ready():
    print(f"🤖 Bot connected as {bot.user}")
    while True:
        try:
            raw = get_mexc_orderbook()
            info = analyze_orderbook(raw)
            msg = (
                f"📊 **BTC/USDT Sniper Watch**\n"
                f"Current Price: **{info['price']}**\n"
                f"💚 Max Bid: {info['max_bid'][1]} @ {info['max_bid'][0]}\n"
                f"❤️ Max Ask: {info['max_ask'][1]} @ {info['max_ask'][0]}"
            )
            print(msg)
            await send_discord_alert(msg)
            await asyncio.sleep(60)  # 1-minute loop
        except Exception as e:
            print(f"❌ Error: {e}")
            await asyncio.sleep(10)

if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
