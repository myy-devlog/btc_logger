# btc_logger.py
import requests
import csv
from datetime import datetime

try:
    res = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot")
    btc_price = res.json()["data"]["amount"]
except Exception as e:
    print("通信エラー:", e)
    btc_price = "取得失敗"

# データをCSVに記録
with open("btc_log.csv", "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([datetime.now().isoformat(), btc_price])

print(f"[記録完了] BTC価格: ${btc_price}")
