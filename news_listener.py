import discord
import re
import os

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

# Your channel name
TARGET_CHANNEL = "macro-news-feed"

# Optional: channel to send sniper news alerts to
ALERT_CHANNEL = "sniper-alerts"

# Trigger keywords
CRYPTO_KEYWORDS = [
    "bitcoin", "btc", "ethereum", "eth", "crypto", "etf", "halving", "binance", "sec", "spot etf", "coinbase"
]
MACRO_KEYWORDS = [
    "inflation", "cpi", "fomc", "rate hike", "interest rate", "fed", "recession", "oil", "war", "conflict", "china", "europe", "israel", "blackrock"
]

@client.event
async def on_ready():
    print(f"✅ News listener bot is running as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.name != TARGET_CHANNEL:
        return

    text = message.content.lower()

    # Scan for keywords
    crypto_hits = [kw for kw in CRYPTO_KEYWORDS if kw in text]
    macro_hits = [kw for kw in MACRO_KEYWORDS if kw in text]

    risk_score = "🟢 LOW"
    if len(macro_hits) > 0:
        risk_score = "🟡 MEDIUM"
    if any(x in text for x in ["war", "explosion", "missile", "crash", "black swan", "emergency"]):
        risk_score = "🔴 HIGH"

    # Compose alert
    if crypto_hits or macro_hits:
        alert_channel = discord.utils.get(message.guild.channels, name=ALERT_CHANNEL)
        if alert_channel:
            await alert_channel.send(
                f"""
🧠 **News Trigger Detected**
> **Headline:** {message.content}
> **Risk Score:** {risk_score}
> **Tags:** {" ".join(set(crypto_hits + macro_hits))}
→ GPT is now operating with adjusted macro awareness.
                """
            )
            print(f"📡 News signal relayed to {ALERT_CHANNEL}")
        else:
            print("⚠️ Alert channel not found.")

# Start the bot
client.run(os.environ["DISCORD_BOT_TOKEN"])
