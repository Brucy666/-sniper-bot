import requests
import os

def get_bybit_price_vwap():
    url = "https://coinalyze-api.p.rapidapi.com/markets/futures/summary"
    headers = {
        "X-RapidAPI-Key": os.getenv("COINALYZE_API_KEY"),
        "X-RapidAPI-Host": "coinalyze-api.p.rapidapi.com"
    }
    params = {"symbol": "BYBIT:BTCUSD"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        data = response.json()
        print("[🔍 Raw Coinalyze Data]", data)  # Debug line

        # Extract VWAP from updated field
        price = float(data["data"]["price"])
        vwap = float(data["data"]["vwap"])

        return price, vwap
    except Exception as e:
        print(f"[VWAP Fetch Error] {e}")
        return None
