import os
import requests

COINCAP_API_KEY = os.getenv("COINCAP_API_KEY", "")
HEADERS = {
    "Authorization": f"Bearer {COINCAP_API_KEY}"
}

def get_coincap_price_vwap():
    try:
        url = "https://api.coincap.io/v2/assets/bitcoin"
        response = requests.get(url, headers=HEADERS)
        data = response.json()

        price = float(data["data"]["priceUsd"])
        vwap = float(data["data"]["vwap24Hr"])
        return price, vwap

    except Exception as e:
        print(f"[CoinCap Fetch Error] {e}")
        return None, None

# ✅ NEW WRAPPER for GPT modules expecting structured return
def get_coincap_data():
    price, vwap = get_coincap_price_vwap()
    return {
        "price": price,
        "vwap": vwap
    }
