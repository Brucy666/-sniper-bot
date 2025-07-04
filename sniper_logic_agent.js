import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

MEXC_API_KEY = os.getenv("MEXC_API_KEY")
MEXC_API_SECRET = os.getenv("MEXC_API_SECRET")

# Base URL for MEXC Spot Market
BASE_URL = "https://api.mexc.com"

# Pairs to track
PAIRS = ["BTCUSDT", "ETHUSDT"]

def fetch_order_book(symbol, limit=20):
    url = f"{BASE_URL}/api/v3/depth"
    params = {"symbol": symbol, "limit": limit}
    res = requests.get(url, params=params)
    return res.json()

def fetch_ticker(symbol):
    url = f"{BASE_URL}/api/v3/ticker/24hr"
    params = {"symbol": symbol}
    res = requests.get(url, params=params)
    return res.json()

def fetch_trades(symbol, limit=20):
    url = f"{BASE_URL}/api/v3/trades"
    params = {"symbol": symbol, "limit": limit}
    res = requests.get(url, params=params)
    return res.json()

def format_wall(orders, side):
    formatted = []
    for price, quantity in orders:
        usdt_val = float(price) * float(quantity)
        if usdt_val > 50000:  # Filter small noise
            formatted.append(f"{side} {price} × {round(usdt_val/1000)}k")
    return formatted

def run_sniper_loop():
    print("\n🔫 MEXC SNIPER BOT STARTED\n")

    while True:
        for pair in PAIRS:
            try:
                ob = fetch_order_book(pair)
                ticker = fetch_ticker(pair)
                trades = fetch_trades(pair)

                price = float(ticker['lastPrice'])
                volume = float(ticker['quoteVolume'])
                buy_trades = [t for t in trades if not t['isBuyerMaker']]
                sell_trades = [t for t in trades if t['isBuyerMaker']]

                print(f"\n[SNIPER] {pair}")
                print(f"📊 Price: {price:.2f} | 24h Vol: {round(volume/1_000_000, 2)}M USDT")

                walls = format_wall(ob['bids'], '🟢') + format_wall(ob['asks'], '🔴')
                for wall in walls[:5]:
                    print(f"   {wall}")

                print(f"💥 Buy Trades: {len(buy_trades)} | Sell Trades: {len(sell_trades)}")
                print("-" * 40)

            except Exception as e:
                print(f"[ERROR] {pair}: {str(e)}")

        time.sleep(10)

if __name__ == "__main__":
    run_sniper_loop()
