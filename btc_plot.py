import csv
from datetime import datetime
import matplotlib.pyplot as plt
import os

# ファイルパス設定
csv_path = r"C:/Users/Mizuki/Documents/cursor/btc_logger/btc_log.csv"
output_folder = r"C:/Users/Mizuki/Documents/cursor/btc_logger/graphs"
plt.rcParams['font.family'] = 'Meiryo'

# データ読み込み
timestamps = []
prices = []

with open(csv_path, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            timestamps.append(datetime.fromisoformat(row[0]))
            prices.append(float(row[1]))
        except:
            continue

# -----------「時刻で昇順ソート」+「重複除外（最新優先）」-----------
# 重複日時を「最後のデータで上書き」
unique_dict = {}
for t, p in zip(timestamps, prices):
    unique_dict[t] = p
# 辞書から「時刻でソートして」リスト化
sorted_items = sorted(unique_dict.items(), key=lambda x: x[0])
timestamps_sorted = [item[0] for item in sorted_items]
prices_sorted = [item[1] for item in sorted_items]

# 直近30件だけ使う
timestamps_final = timestamps_sorted[-30:]
prices_final = prices_sorted[-30:]

# 統計情報
if prices_final:
    avg_price = sum(prices_final) / len(prices_final)
    max_price = max(prices_final)
    min_price = min(prices_final)
    print(f"📊 統計情報（直近{len(prices_final)}件）")
    print(f"平均価格：{avg_price:.2f} USD")
    print(f"最高価格：{max_price:.2f} USD")
    print(f"最安価格：{min_price:.2f} USD")
else:
    print("価格データが存在しません。")
    exit()

# 折れ線グラフ描画（X軸は昇順で綺麗に）
plt.figure(figsize=(10, 5))
plt.plot(timestamps_final, prices_final, marker='o', linestyle='-', color='dodgerblue', label='価格の推移（折れ線グラフ）')
plt.axhline(y=avg_price, color='orange', linestyle='--', label=f'平均 {avg_price:.2f} USD')
plt.title("BTC価格の推移")
plt.xlabel("日時")
plt.ylabel("価格 (USD)")
plt.grid(True)
plt.legend(fontsize=10)
plt.tight_layout()
plt.subplots_adjust(bottom=0.20)
plt.xticks(fontsize=8, rotation=45)

os.makedirs(output_folder, exist_ok=True)
today_str = datetime.now().strftime("%Y-%m-%d")
output_path = os.path.join(output_folder, f"{today_str}_line.png")
plt.savefig(output_path)
print(f"✅ グラフを保存しました: {output_path}")
