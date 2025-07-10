import requests
import os

def get_coincap_price_vwap():
    url = "https://api.coincap.io/v2/assets/bitcoin"
    headers = {
        "Authorization": f"Bearer {os.environ.get('COINCAP_API_KEY')}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        price = float(data["data"]["priceUsd"])
        vwap = float(data["data"]["vwap24Hr"])

        return price, vwap
    except Exception as e:
        print(f"[CoinCap Fetch Error] {e}")
        return None
