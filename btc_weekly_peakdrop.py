import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

# =========================
# 🟢 凡例位置の選択
# =========================
legend_options = {
    "1": "upper right",
    "2": "upper left",
    "3": "lower left",
    "4": "lower right"
}
print("凡例の位置を選んでください：")
print("1: 右上, 2: 左上, 3: 左下, 4: 右下")
loc_input = input("選択番号（1〜4）: ").strip()
legend_loc = legend_options.get(loc_input, "upper right")

# =========================
# 🟢 週の基準日を指定（空欄なら今日）
# =========================
print("週の基準日を入力してください（例: 2024-05-27）")
date_input = input("未入力なら今週を使用: ").strip()
try:
    base_date = datetime.strptime(date_input, "%Y-%m-%d").date()
except:
    base_date = datetime.now().date()

monday = base_date - timedelta(days=base_date.weekday())
sunday = monday + timedelta(days=6)

# =========================
# 🟢 ファイル設定
# =========================
csv_path = r"C:/Users/Mizuki/Documents/cursor/btc_logger/btc_log.csv"
output_folder = r"C:/Users/Mizuki/Documents/cursor/btc_logger/graphs"
plt.rcParams['font.family'] = 'Meiryo'

# =========================
# 🟢 CSV読み込み
# =========================
timestamps, prices = [], []
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            timestamps.append(datetime.fromisoformat(row[0]))
            prices.append(float(row[1]))
        except:
            continue

# 重複除去＆ソート
unique_dict = {t: p for t, p in zip(timestamps, prices)}
timestamps_sorted = sorted(unique_dict.keys())
prices_sorted = [unique_dict[t] for t in timestamps_sorted]

# =========================
# 🟢 指定週のデータ抽出
# =========================
week_timestamps = []
week_prices = []
for t, p in zip(timestamps_sorted, prices_sorted):
    if monday <= t.date() <= sunday:
        week_timestamps.append(t)
        week_prices.append(p)

if not week_prices:
    print("⚠️ 指定週のデータが見つかりません。")
    exit()

# =========================
# 🟢 DataFrame・指標計算
# =========================
df = pd.DataFrame({"timestamp": week_timestamps, "price": week_prices})
df["date"] = df["timestamp"].dt.date
all_dates = [monday + timedelta(days=i) for i in range(7)]
day_avg = df.groupby("date")["price"].mean().reindex(all_dates)

week_avg = np.mean(week_prices)
week_max = np.max(week_prices)
week_min = np.min(week_prices)
max_idx = np.argmax(week_prices)
min_idx = np.argmin(week_prices)

price_diffs = np.diff(week_prices)
max_up_idx = np.argmax(price_diffs) + 1
max_down_idx = np.argmin(price_diffs) + 1
max_up_val = price_diffs[max_up_idx - 1]
max_down_val = price_diffs[max_down_idx - 1]
max_up_percent = (max_up_val / week_prices[max_up_idx - 1]) * 100 if week_prices[max_up_idx - 1] != 0 else 0
max_down_percent = (max_down_val / week_prices[max_down_idx - 1]) * 100 if week_prices[max_down_idx - 1] != 0 else 0

# =========================
# 🟢 グラフ描画
# =========================
plt.figure(figsize=(10, 6))
plt.plot(df["timestamp"], df["price"], linestyle='-', color='lightgray', alpha=0.7)
plt.plot([datetime.combine(d, datetime.min.time()) for d in day_avg.index], day_avg.values,
         marker='o', color='dodgerblue', linewidth=2, label="日別平均")
plt.axhline(y=week_avg, color='orange', linestyle='--', label=f'週平均 {week_avg:,.0f} USD')
plt.axhline(y=week_max, color='red', linestyle='--')
plt.axhline(y=week_min, color='green', linestyle='--')

# 高値・底値
plt.scatter([week_timestamps[max_idx]], [week_prices[max_idx]], color='red')
plt.text(week_timestamps[max_idx], week_prices[max_idx], f"高値 {week_max:,.2f} USD",
         color='red', fontsize=10, ha='left', va='bottom')
plt.scatter([week_timestamps[min_idx]], [week_prices[min_idx]], color='green')
plt.text(week_timestamps[min_idx], week_prices[min_idx], f"底値 {week_min:,.2f} USD",
         color='green', fontsize=10, ha='left', va='top')

# 最大上昇・下落（矢印＋注釈）
def plot_arrow_annotate(x0, x1, y0, y1, color, label, offset_ratio):
    mid_x = x0 + (x1 - x0) / 2
    mid_y = y0 + (y1 - y0) / 2
    plt.annotate('', xy=(x1, y1), xytext=(x0, y0),
                 arrowprops=dict(arrowstyle='<->', color=color, lw=1.5))
    plt.text(mid_x, mid_y * offset_ratio, label,
             ha='center', va='bottom' if offset_ratio > 1 else 'top',
             fontsize=10, color=color)

plot_arrow_annotate(
    week_timestamps[max_up_idx - 1], week_timestamps[max_up_idx],
    week_prices[max_up_idx - 1], week_prices[max_up_idx],
    'magenta', f"{max_up_percent:+.2f}%\n▲+{max_up_val:,.2f} USD", 1.01
)

plot_arrow_annotate(
    week_timestamps[max_down_idx - 1], week_timestamps[max_down_idx],
    week_prices[max_down_idx - 1], week_prices[max_down_idx],
    'deepskyblue', f"{max_down_percent:+.2f}%\n▼{abs(max_down_val):,.2f} USD", 0.99
)

# =========================
# 🟢 凡例
# =========================
legend_lines = [
    Line2D([0], [0], color='lightgray', label="時間ごとの価格"),
    Line2D([0], [0], color='dodgerblue', marker='o', label="日別平均"),
    Line2D([0], [0], color='orange', linestyle='--', label=f"週平均 {week_avg:,.0f} USD"),
    Line2D([0], [0], color='red', marker='o', linestyle='--', label=f"高値 {week_max:,.2f} USD"),
    Line2D([0], [0], color='green', marker='o', linestyle='--', label=f"底値 {week_min:,.2f} USD"),
    Line2D([0], [0], color='magenta', linestyle='-', label=(
        f"最大上昇: {week_timestamps[max_up_idx - 1].strftime('%Y-%m-%d %H:%M')}~"
        f"{week_timestamps[max_up_idx].strftime('%H:%M')} (JST)  "
        f"{week_prices[max_up_idx - 1]:,.2f}→{week_prices[max_up_idx]:,.2f} "
        f"({max_up_percent:+.2f}%)"
    )),
    Line2D([0], [0], color='deepskyblue', linestyle='-', label=(
        f"最大下落: {week_timestamps[max_down_idx - 1].strftime('%Y-%m-%d %H:%M')}~"
        f"{week_timestamps[max_down_idx].strftime('%H:%M')} (JST)  "
        f"{week_prices[max_down_idx - 1]:,.2f}→{week_prices[max_down_idx]:,.2f} "
        f"({max_down_percent:+.2f}%)"
    ))
]

plt.title(f"BTC週次平均価格（{monday}～{sunday}）")
plt.xlabel("日付")
plt.ylabel("価格 (USD)")
plt.grid(True)
plt.legend(handles=legend_lines, loc=legend_loc, fontsize=9)

# X軸整形
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gcf().autofmt_xdate()

# 保存
os.makedirs(output_folder, exist_ok=True)
filename = f"weekavg_{monday.strftime('%Y-%m-%d')}_peakdrop.png"
plt.tight_layout()
plt.savefig(os.path.join(output_folder, filename))
plt.close()
print(f"✅ グラフを保存しました: {filename}（凡例位置: {legend_loc}）")
