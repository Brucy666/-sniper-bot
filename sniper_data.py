import requests
import os

def get_bybit_price_vwap():
    url = "https://coinalyze-api.p.rapidapi.com/bybit/futures/get-spot-summary"
    headers = {
        "X-RapidAPI-Key": os.getenv("COINALYZE_API_KEY", ""),
        "X-RapidAPI-Host": "coinalyze-api.p.rapidapi.com"
    }

    params = {"symbol": "BYBIT:BTCUSDT"}  # 🛠️ Correct symbol format

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()  # Throw error on bad HTTP status
        data = response.json()

        print("✅ Raw Coinalyze Data:", data)

        price = float(data["price"])
        vwap = float(data["vwap"])

        return price, vwap

    except Exception as e:
        print(f"❌ VWAP Fetch Error → {e}")
        return None
