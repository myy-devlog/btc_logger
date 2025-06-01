import os
import requests
from datetime import datetime, timedelta, timezone
import pandas as pd
import time

# 保存先
save_dir = "btc_logger"
os.makedirs(save_dir, exist_ok=True)
csv_path = os.path.join(save_dir, "btc_log.csv")

# タイムゾーン設定
JST = timezone(timedelta(hours=9))
now_utc = datetime.utcnow()
one_year_ago_utc = now_utc - timedelta(days=365)
utc_limit = now_utc - timedelta(hours=1)

# 既存データの読み込みと整形
existing_timestamps = set()
if os.path.exists(csv_path):
    existing_df = pd.read_csv(csv_path, names=["timestamp", "price"])
    existing_df["timestamp"] = pd.to_datetime(existing_df["timestamp"], utc=True).dt.tz_convert(JST)
    existing_df["timestamp"] = existing_df["timestamp"].apply(lambda dt: dt.isoformat())
    existing_timestamps = set(existing_df["timestamp"].tolist())
else:
    existing_df = pd.DataFrame(columns=["timestamp", "price"])

# 欠損補完対象となる全時間帯を列挙
full_range = pd.date_range(
    start=one_year_ago_utc,
    end=utc_limit,
    freq='h',
    tz='UTC'
)
missing_datetimes = [
    dt for dt in full_range
    if dt.astimezone(JST).isoformat() not in existing_timestamps
]

print(f"📅 補完対象の時刻数: {len(missing_datetimes)}")

# Binance APIから1時間足データ取得
def fetch_binance_data(start_time, end_time):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": "BTCUSDT",
        "interval": "1h",
        "startTime": int(start_time.timestamp() * 1000),
        "endTime": int(end_time.timestamp() * 1000),
        "limit": 1000
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

# データ取得
all_new_rows = []
current = one_year_ago_utc
while current < utc_limit:
    chunk_end = min(current + timedelta(hours=1000), utc_limit)
    try:
        candles = fetch_binance_data(current, chunk_end)
    except Exception as e:
        print("❌ API取得エラー:", e)
        break

    for c in candles:
        ts_utc = datetime.utcfromtimestamp(c[0] / 1000).replace(tzinfo=timezone.utc)
        ts_jst = ts_utc.astimezone(JST).replace(minute=0, second=0, microsecond=0)
        iso_jst = ts_jst.isoformat()  # 厳密なISO形式：例 2025-06-01T00:00:00+09:00
        if iso_jst not in existing_timestamps:
            price = float(c[4])  # 終値
            all_new_rows.append([iso_jst, price])

    current = chunk_end
    time.sleep(0.1)

# 保存処理
new_df = pd.DataFrame(all_new_rows, columns=["timestamp", "price"])
combined_df = pd.concat([existing_df, new_df], ignore_index=True)
combined_df.drop_duplicates(subset=["timestamp"], inplace=True)

# datetimeとしてソート
combined_df["timestamp_dt"] = pd.to_datetime(combined_df["timestamp"])
combined_df.sort_values(by="timestamp_dt", inplace=True)
combined_df.drop(columns=["timestamp_dt"], inplace=True)

combined_df.to_csv(csv_path, index=False, header=False)

# 出力確認
print(f"✅ Binanceから {len(new_df)} 件の新データを追加（JST）")
print(f"📁 保存先: {csv_path}")
if not new_df.empty:
    print(new_df.head())
else:
    print(f"ℹ️ 1年分はすべて取得済みです（～ {utc_limit.astimezone(JST):%Y-%m-%d %H:%M} JST）")
