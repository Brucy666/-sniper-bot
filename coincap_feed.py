# coincap_feed.py

import httpx
import os

COINCAP_API_KEY = os.environ.get("COINCAP_API_KEY")
COINCAP_API_URL = "https://api.coincap.io/v2/assets/bitcoin"

headers = {
    "Authorization": f"Bearer {COINCAP_API_KEY}"
}

async def get_coincap_data():
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(COINCAP_API_URL, headers=headers)
            res.raise_for_status()
            data = res.json()["data"]
            return {
                "price": float(data["priceUsd"]),
                "vwap": float(data["vwap24Hr"])
            }
    except Exception as e:
        print(f"[CoinCap Fetch Error] {e}")
        return {"price": None, "vwap": None}
