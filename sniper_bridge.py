# sniper_bridge.py

import json
import os
import asyncio
from datetime import datetime, timedelta
from fastapi import FastAPI
from pydantic import BaseModel
import discord

# === Setup ===
MEMORY_FILE = "macro_risk_memory.json"
STATUS_FILE = "sniper_status.json"
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
DISCORD_CHANNEL = "sniper-alerts"

app = FastAPI()

# === Input Model from TradingView Webhook ===
class TradingViewAlert(BaseModel):
    event: str
    price: float | None = None
    trigger: str | None = None
    rsi: float | None = None
    notes: str | None = None

# === Macro Memory Logic ===
def get_macro_risk():
    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
        if data.get("macro_risk_last_updated"):
            last = datetime.fromisoformat(data["macro_risk_last_updated"])
            now = datetime.utcnow()
            delta = now - last
            if data["macro_risk_score"] == "🔴 HIGH" and delta > timedelta(minutes=15):
                print("⏱️ Risk decayed: 🔴 HIGH → 🟡 MEDIUM")
                data["macro_risk_score"] = "🟡 MEDIUM"
            elif data["macro_risk_score"] == "🟡 MEDIUM" and delta > timedelta(minutes=15):
                print("⏱️ Risk decayed: 🟡 MEDIUM → 🟢 LOW")
                data["macro_risk_score"] = "🟢 LOW"
        return data
    except FileNotFoundError:
        return {
            "macro_risk_score": "🟢 LOW",
            "macro_risk_tags": [],
            "macro_risk_last_updated": None
        }

# === Terminal Overlay ===
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
→ Entry Delayed       : {"✅ Yes" if delay else "❌ No"}
→ Macro Overlay       : {"⚠️ Risk Pressure Active" if delay else "🟢 Clear"}
""")

# === Discord Alert ===
async def send_discord_alert(message: str):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        ch = discord.utils.get(client.get_all_channels(), name=DISCORD_CHANNEL)
        if ch:
            await ch.send(message)
        await client.close()
        await asyncio.sleep(1)

    await client.start(DISCORD_TOKEN)

def save_status(status):
    with open(STATUS_FILE, "w") as f:
        json.dump({"status": status}, f)

def load_status():
    try:
        with open(STATUS_FILE, "r") as f:
            return json.load(f).get("status", "UNKNOWN")
    except:
        return "UNKNOWN"

# === Webhook Handler ===
@app.post("/webhook")
async def handle_alert(alert: TradingViewAlert):
    print(f"🚨 Received Alert: {alert.event} | Price: {alert.price} | RSI: {alert.rsi}")

    # === Confidence Logic ===
    base_conf = 85
    confidence = base_conf
    delay = False

    # Macro Risk Score
    macro = get_macro_risk()
    score = macro["macro_risk_score"]
    tags = macro["macro_risk_tags"]
    updated = macro["macro_risk_last_updated"]

    if score == "🔴 HIGH":
        confidence -= 25
        delay = True
    elif score == "🟡 MEDIUM":
        confidence -= 10

    print_terminal_overlay(score, tags, updated, base_conf, confidence, delay)

    # === Sniper Status Tracking ===
    new_status = "BLOCKED" if delay else "ALLOWED"
    old_status = load_status()

    if new_status != old_status:
        save_status(new_status)
        message = f"""
{'⚠️ **Sniper Entry Blocked**' if new_status == 'BLOCKED' else '🔓 **Sniper Entry Unlocked**'}
→ Macro Risk: {score}
→ Confidence: {confidence}%
→ {'Sniper suppressed by GPT defense layer' if new_status == 'BLOCKED' else 'All systems rearmed ✅'}
"""
        await send_discord_alert(message)

    # === Final Webhook Response ===
    return {
        "status": "ok",
        "confidence": confidence,
        "entry_allowed": not delay
    }

# === Run Locally ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("sniper_bridge:app", host="0.0.0.0", port=8000, reload=True)
