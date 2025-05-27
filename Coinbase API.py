import requests

res = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot")
btc_price = res.json()["data"]["amount"]
print(f"Coinbaseから取得：現在のBTC価格：${btc_price}")

