from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
import json
from datetime import datetime

app = FastAPI()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MEMORY_FILE = "macro_risk_memory.json"

class WebhookPayload(BaseModel):
    event: str
    wallet: str = None
    token: str = None
    rsi: float = None
    vwap_status: str = None
    extra_info: str = None

class MemoryUpdate(BaseModel):
    score: str
    tags: list[str]

@app.post("/webhook")
async def handle_webhook(payload: WebhookPayload):
    message = f"""
    Sniper Event Detected:
    - Event: {payload.event}
    - Wallet: {payload.wallet}
    - Token: {payload.token}
    - RSI: {payload.rsi}
    - VWAP Status: {payload.vwap_status}
    - Extra Info: {payload.extra_info or 'None'}

    Based on sniper logic, provide a trade response, confidence score, and next action.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a sniper trade engine."},
            {"role": "user", "content": message}
        ]
    )
    reply = response.choices[0].message.content
    return {"status": "received", "gpt_response": reply}

@app.get("/memory_status")
async def memory_status():
    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
        return {"status": "ok", "memory": data}
    except FileNotFoundError:
        return {"status": "no_file", "memory": None}

@app.post("/update_memory")
async def update_memory(update: MemoryUpdate):
    data = {
        "macro_risk_score": update.score,
        "macro_risk_tags": update.tags,
        "macro_risk_last_updated": datetime.utcnow().isoformat()
    }
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return {"status": "updated", "memory": data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("sniper_bridge:app", host="0.0.0.0", port=8000, reload=True)
