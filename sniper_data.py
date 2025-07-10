import requests
import os

def get_bybit_price_vwap():
    url = "https://coinalyze.com/api/v1/bybit/futures/get-spot-summary?symbol=BYBIT:BTCUSD"
    headers = {
        "api_key": os.getenv("COINALYZE_API_KEY")
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        print("🧠 Raw Coinalyze Data", data)

        price = float(data["price"])
        vwap = float(data["vwap"])

        return price, vwap

    except Exception as e:
        print(f"[VWAP Fetch Error] {e}")
        return None
