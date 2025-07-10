# coincap_feed.py

import httpx
import os

COINCAP_API_KEY = os.environ.get("COINCAP_API_KEY")
COINCAP_API_URL = "https://api.coincap.io/v2/assets/bitcoin"

headers = {
    "Authorization": f"Bearer {COINCAP_API_KEY}"
}

async def get_coincap_price_vwap():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(COINCAP_API_URL, headers=headers)
            response.raise_for_status()
            data = response.json()["data"]

            price = float(data.get("priceUsd", 0))
            vwap = float(data.get("vwap24Hr", 0))

            return price, vwap

    except Exception as e:
        print(f"[CoinCap Fetch Error] {e}")
        return None, None

async def get_coincap_data():
    price, vwap = await get_coincap_price_vwap()
    return {"price": price, "vwap": vwap}
