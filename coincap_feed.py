import os
import requests

COINCAP_API_KEY = os.environ.get("COINCAP_API_KEY", "")
BASE_URL = "https://api.coincap.io/v2/assets/bitcoin"

def get_coincap_data():
    headers = {
        "Authorization": f"Bearer {COINCAP_API_KEY}"
    }
    try:
        response = requests.get(BASE_URL, headers=headers)
        response.raise_for_status()
        data = response.json().get("data", {})

        price = float(data.get("priceUsd", 0))
        vwap = float(data.get("vwap24Hr", 0))

        if price and vwap:
            return {
                "price": price,
                "vwap": vwap
            }
        else:
            print("❌ VWAP or price missing from CoinCap response.")
            return None
    except Exception as e:
        print(f"[CoinCap Fetch Error] {e}")
        return None
