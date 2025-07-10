import requests
import os

def get_coincap_price_vwap():
    url = "https://api.coincap.io/v2/assets/bitcoin"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        price = float(data["data"]["priceUsd"])
        vwap = float(data["data"]["vwap24Hr"])
        return price, vwap
    except Exception as e:
        print(f"[CoinCap Fetch Error] {e}")
        return None
