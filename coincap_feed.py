import requests
import os

COINCAP_API_KEY = os.getenv("COINCAP_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {COINCAP_API_KEY}"
}

def get_coincap_price_vwap():
    url = "https://api.coincap.io/v2/assets/bitcoin"
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        response.raise_for_status()
        data = response.json()
        price = float(data["data"]["priceUsd"])
        vwap = float(data["data"]["vwap24Hr"])
        return price, vwap
    except Exception as e:
        print(f"[CoinCap Fetch Error] {e}")
        return None

def get_coincap_data():
    url = "https://api.coincap.io/v2/assets"
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[CoinCap General Error] {e}")
        return None
