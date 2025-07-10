# coincap_feed.py

import httpx
import os

COINCAP_API_KEY = os.environ.get("COINCAP_API_KEY")
COINCAP_API_URL = "https://api.coincap.io/v2/assets/bitcoin"

headers = {
    "Authorization": f"Bearer {COINCAP_API_KEY}"
}

async def get_coincap_price_vwap():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(COINCAP_API_URL, headers=headers)
            response.raise_for_status()
            data = response.json()["data"]

            price = float(data["priceUsd"])
            vwap = float(data["vwap24Hr"])

            return price, vwap

        except Exception as e:
            print(f"[CoinCap Fetch Error] {e}")
            return None, None

def get_coincap_data():
    import asyncio
    price, vwap = asyncio.run(get_coincap_price_vwap())
    return {"price": price, "vwap": vwap}
