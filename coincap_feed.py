import requests
import os

def get_coincap_price_vwap():
    """
    Fetches current Bitcoin price and 24Hr VWAP from CoinCap API.

    Returns:
        tuple: (price, vwap) as floats
    """
    url = "https://api.coincap.io/v2/assets/bitcoin"
    headers = {
        "Authorization": f"Bearer {os.environ.get('COINCAP_API_KEY', '')}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json().get("data", {})

        price = float(data.get("priceUsd", 0))
        vwap = float(data.get("vwap24Hr", 0))

        return price, vwap

    except Exception as e:
        print(f"[CoinCap Fetch Error] {e}")
        return None, None
