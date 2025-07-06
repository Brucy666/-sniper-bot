import requests

url = "https://sniper-bridge.up.railway.app/webhook"

payload = {
    "event": "wallet_rsi_alert",
    "wallet": "⚡️ ShockedJS",
    "token": "WOOF",
    "rsi": 29.1,
    "vwap_status": "below",
    "extra_info": "Volume spike detected"
}

response = requests.post(url, json=payload)
print("Response:", response.status_code)
print(response.json())
