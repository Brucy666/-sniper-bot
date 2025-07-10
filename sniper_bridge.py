import json
import os
from datetime import datetime, timedelta
import discord
import asyncio
from coincap_feed import get_coincap_price_vwap  # NEW: using CoinCap

# === Config ===
MEMORY_FILE = "macro_risk_memory.json"
STATUS_FILE = "sniper_status.json"
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
DISCORD_CHANNEL = "sniper-alerts"

# === Risk Memory Logic ===
def get_macro_risk():
    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
        last = datetime.fromisoformat(data.get("macro_risk_last_updated", "")) if data.get("macro_risk_last_updated") else None
        if last:
            elapsed = datetime.utcnow() - last
            if data["macro_risk_score"] == "🔴 HIGH" and elapsed > timedelta(minutes=15):
                print("⏱️ Risk decayed: 🔴 HIGH → 🟡 MEDIUM")
                data["macro_risk_score"] = "🟡 MEDIUM"
            elif data["macro_risk_score"] == "🟡 MEDIUM" and elapsed > timedelta(minutes=15):
                print("⏱️ Risk decayed: 🟡 MEDIUM → 🟢 LOW")
                data["macro_risk_score"] = "🟢 LOW"
        return data
    except:
        print("[⚠️] No macro memory found. Returning default.")
        return {
            "macro_risk_score": "🟢 LOW",
            "macro_risk_tags": [],
            "macro_risk_last_updated": None
        }

def save_status(status):
    with open(STATUS_FILE, "w") as f:
        json.dump({"status": status}, f)

def load_status():
    try:
        with open(STATUS_FILE, "r") as f:
            return json.load(f).get("status", "UNKNOWN")
    except:
        return "UNKNOWN"

def print_terminal_overlay(score, tags, updated, base_conf, adjusted_conf, delay):
    print(f"""
🧠 GPT Macro Memory Loaded
────────────────────────────
→ Score        : {score}
→ Tags         : {tags}
→ Last Updated : {updated}

🎯 Sniper Decision Check
────────────────────────────
→ Base Confidence     : {base_conf}%
→ Adjusted Confidence : {adjusted_conf}%
→ Entry Delayed       : {"❌ No" if not delay else "✅ Yes"}
→ Macro Overlay       : {"🟢 Clear" if not delay else "⚠️ Risk Pressure Active"}
""")

async def send_discord_alert(message):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        ch = discord.utils.get(client.get_all_channels(), name=DISCORD_CHANNEL)
        if ch:
            await ch.send(message)
        await client.close()

    await client.start(DISCORD_TOKEN)

# === Core Execution ===
base_conf = 85
sniper_conf = base_conf
delay_entry = False

try:
    result = get_coincap_price_vwap()
    if result:
        price, vwap = result
        print(f"📈 Price: {price} | 📊 VWAP: {vwap}")
        if price > vwap:
            sniper_conf += 5
        elif price < vwap:
            sniper_conf -= 5
    else:
        print("❌ CoinCap VWAP fetch failed")
except Exception as e:
    print(f"[VWAP Fetch Error] {e}")

risk = get_macro_risk()
score = risk["macro_risk_score"]
tags = risk["macro_risk_tags"]
updated = risk["macro_risk_last_updated"]

if score == "🔴 HIGH":
    sniper_conf -= 25
    delay_entry = True
elif score == "🟡 MEDIUM":
    sniper_conf -= 10

print_terminal_overlay(score, tags, updated, base_conf, sniper_conf, delay_entry)

# === Entry Status Update ===
new_status = "BLOCKED" if delay_entry else "ALLOWED"
old_status = load_status()

if new_status != old_status:
    print(f"🔁 Sniper status changed: {old_status} → {new_status}")
    save_status(new_status)

    alert = f"""
{'⚠️ **Sniper Entry Blocked**' if new_status == 'BLOCKED' else '🔓 **Sniper Entry Unlocked**'}
→ Macro Risk: {score}
→ Confidence: {sniper_conf}%
→ {'Sniper suppressed by GPT defense layer' if new_status == 'BLOCKED' else 'All systems rearmed ✅'}
"""
    asyncio.run(send_discord_alert(alert))
