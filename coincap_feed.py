# coincap_feed.py

import os
import asyncio
import httpx

COINCAP_API_KEY = os.getenv("COINCAP_API_KEY")
COINCAP_API_URL = "https://api.coincap.io/v2/assets/bitcoin"

HEADERS = {
    "Authorization": f"Bearer {COINCAP_API_KEY}"
}


async def fetch_coincap_price_vwap():
    """
    Asynchronously fetch price and VWAP for Bitcoin from CoinCap API.

    Returns:
        tuple: (price: float, vwap: float) or (None, None) on failure
    """
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(COINCAP_API_URL, headers=HEADERS)
            response.raise_for_status()
            data = response.json().get("data", {})
            price = float(data.get("priceUsd", 0))
            vwap = float(data.get("vwap24Hr", 0))
            return price, vwap
    except Exception as e:
        print(f"[CoinCap Fetch Error] {e}")
        return None, None


def get_coincap_data():
    """
    Synchronously get CoinCap price and VWAP using async wrapper.

    Returns:
        dict: {"price": float or None, "vwap": float or None}
    """
    try:
        price, vwap = asyncio.run(fetch_coincap_price_vwap())
        return {"price": price, "vwap": vwap}
    except Exception as e:
        print(f"[CoinCap Wrapper Error] {e}")
        return {"price": None, "vwap": None}
