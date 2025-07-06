from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class WebhookPayload(BaseModel):
    event: str
    wallet: str = None
    token: str = None
    rsi: float = None
    vwap_status: str = None
    extra_info: str = None

@app.post("/webhook")
async def handle_webhook(payload: WebhookPayload):
    # Build a smart GPT prompt from the webhook input
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

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a sniper trade engine."},
                  {"role": "user", "content": message}]
    )

    reply = response['choices'][0]['message']['content']
    return {"status": "received", "gpt_response": reply}
