import requests
import os

def get_bybit_price_vwap():
    url = "https://coinalyze-api.p.rapidapi.com/bybit/summary"
    headers = {
        "X-RapidAPI-Key": os.getenv("COINALYZE_API_KEY"),
        "X-RapidAPI-Host": "coinalyze-api.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        print("🔘 Raw Coinalyze Data:", data)

        price = float(data["data"]["lastPrice"])
        vwap = float(data["data"]["vwap"])
        return price, vwap

    except Exception as e:
        print(f"[VWAP Fetch Error] {e}")
        return None
