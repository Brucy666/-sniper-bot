import requests
import os

def get_bybit_price_vwap():
    api_key = "671f76e0-53d2-432b-a57a-afbd6d89fd48"
    url = f"https://coinalyze.net/api/v1/bybit/futures/get-spot-summary?symbol=BYBIT:BTCUSD&api_key={api_key}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        print("🧠 Raw Coinalyze Data", data)

        price = float(data["price"])
        vwap = float(data["vwap"])

        return price, vwap

    except Exception as e:
        print(f"[VWAP Fetch Error] {e}")
        print("❌ Failed to fetch Bybit VWAP data (invalid format)")
        return None
