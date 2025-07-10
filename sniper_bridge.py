 # sniper_bridge.py

import os
import json
from datetime import datetime, timedelta
from fastapi import FastAPI, Request
import discord
import asyncio

MEMORY_FILE = "macro_risk_memory.json"
STATUS_FILE = "sniper_status.json"

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL = os.getenv("DISCORD_CHANNEL_ID", "sniper-alerts")

# === FastAPI app ===
app = FastAPI()

# === Discord Client ===
discord_client = discord.Client(intents=discord.Intents.default())

# === Risk Memory ===
def get_macro_risk():
    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
        if data.get("macro_risk_last_updated"):
            last = datetime.fromisoformat(data["macro_risk_last_updated"])
            delta = datetime.utcnow() - last
            if data["macro_risk_score"] == "🔴 HIGH" and delta > timedelta(minutes=15):
                data["macro_risk_score"] = "🟡 MEDIUM"
            elif data["macro_risk_score"] == "🟡 MEDIUM" and delta > timedelta(minutes=15):
                data["macro_risk_score"] = "🟢 LOW"
        return data
    except FileNotFoundError:
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

async def send_discord_alert(message):
    await discord_client.wait_until_ready()
    for ch in discord_client.get_all_channels():
        if ch.name == DISCORD_CHANNEL or str(ch.id) == DISCORD_CHANNEL:
            await ch.send(message)
            break

# === Sniper Logic ===
def run_sniper_check(price, vwap):
    base = 85
    score = get_macro_risk()["macro_risk_score"]
    delay = False

    conf = base + 5 if price > vwap else base - 5
    if score == "🔴 HIGH":
        conf -= 25
        delay = True
    elif score == "🟡 MEDIUM":
        conf -= 10

    new_status = "BLOCKED" if delay else "ALLOWED"
    old_status = load_status()
    if new_status != old_status:
        save_status(new_status)
        return {
            "change": True,
            "message": f"""
{'⚠️ **Sniper Entry Blocked**' if new_status == 'BLOCKED' else '🔓 **Sniper Entry Unlocked**'}
→ Macro Risk: {score}
→ Confidence: {conf}%
→ {'Sniper suppressed by GPT defense layer' if new_status == 'BLOCKED' else 'All systems rearmed ✅'}
"""
        }
    return {"change": False}

# === API Endpoint ===
@app.post("/alert/vwap")
async def handle_alert(req: Request):
    try:
        payload = await req.json()
        price = float(payload.get("price"))
        vwap = float(payload.get("vwap"))
        print(f"🚨 Alert received | Price: {price} | VWAP: {vwap}")

        result = run_sniper_check(price, vwap)
        if result["change"]:
            await send_discord_alert(result["message"])
        return {"status": "ok", "result": result}
    except Exception as e:
        print(f"[Webhook Error] {e}")
        return {"status": "error", "detail": str(e)}

# === Launch Discord client only ===
@discord_client.event
async def on_ready():
    print(f"✅ Discord bot ready as {discord_client.user}")

# === ENTRYPOINT ===
def start():
    import uvicorn
    loop = asyncio.get_event_loop()
    loop.create_task(discord_client.start(DISCORD_TOKEN))
    uvicorn.run("sniper_bridge:app", host="0.0.0.0", port=8000, reload=False)
