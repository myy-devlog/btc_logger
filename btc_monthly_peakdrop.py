import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

csv_path = r"C:/Users/Mizuki/Documents/cursor/btc_logger/btc_log.csv"
output_folder = r"C:/Users/Mizuki/Documents/cursor/btc_logger/graphs"
plt.rcParams['font.family'] = 'Meiryo'

# 🔽 凡例の位置選択
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

# 🔽 年月指定
year = int(input("レポートの年を入力してください（例: 2025）: "))
month = int(input("レポートの月を入力してください（1〜12）: "))
first_day = datetime(year, month, 1)
next_month = first_day.replace(day=28) + timedelta(days=4)
last_day = (next_month - timedelta(days=next_month.day)).date()

# 🔽 データ読み込み
timestamps, prices = [], []
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            t = datetime.fromisoformat(row[0])
            if first_day.date() <= t.date() <= last_day:
                timestamps.append(t)
                prices.append(float(row[1]))
        except:
            continue

if not prices:
    print(f"{year}年{month}月のデータが見つかりませんでした。")
    exit()

df = pd.DataFrame({"timestamp": timestamps, "price": prices})
df["date"] = df["timestamp"].dt.date
day_avg = df.groupby("date")["price"].mean()

# 🔽 指標計算
month_avg = np.mean(prices)
month_max = np.max(prices)
month_min = np.min(prices)
max_idx = np.argmax(prices)
min_idx = np.argmin(prices)

price_diffs = np.diff(prices)
max_up_idx = np.argmax(price_diffs) + 1
max_down_idx = np.argmin(price_diffs) + 1

max_up_val = price_diffs[max_up_idx - 1]
max_up_percent = (max_up_val / prices[max_up_idx - 1]) * 100 if prices[max_up_idx - 1] != 0 else 0
max_up_label = f"{timestamps[max_up_idx - 1].strftime('%Y-%m-%d %H:%M')}~{timestamps[max_up_idx].strftime('%H:%M')}(JST) {prices[max_up_idx - 1]:,.2f}→{prices[max_up_idx]:,.2f} ({max_up_percent:+.2f}%)"

max_down_val = price_diffs[max_down_idx - 1]
max_down_percent = (max_down_val / prices[max_down_idx - 1]) * 100 if prices[max_down_idx - 1] != 0 else 0
max_down_label = f"{timestamps[max_down_idx - 1].strftime('%Y-%m-%d %H:%M')}~{timestamps[max_down_idx].strftime('%H:%M')}(JST) {prices[max_down_idx - 1]:,.2f}→{prices[max_down_idx]:,.2f} ({max_down_percent:+.2f}%)"

# 🔽 グラフ作成
plt.figure(figsize=(12, 6))
line_main, = plt.plot(df["timestamp"], df["price"], linestyle='-', color='lightgray', alpha=0.7, label="価格推移（1時間毎）")
line_dayavg, = plt.plot([datetime.combine(d, datetime.min.time()) for d in day_avg.index], day_avg.values,
                        marker='o', color='cornflowerblue', linewidth=2, label="日別平均")
line_avg = plt.axhline(y=month_avg, color='orange', linestyle='--', label=f'月平均 {month_avg:,.0f} USD')
line_max = plt.axhline(y=month_max, color='red', linestyle='--', linewidth=1)
line_min = plt.axhline(y=month_min, color='green', linestyle='--', linewidth=1)

# 🔽 高値・底値
plt.scatter([timestamps[max_idx]], [prices[max_idx]], color='red', zorder=5)
plt.scatter([timestamps[min_idx]], [prices[min_idx]], color='green', zorder=5)
plt.annotate(f"高値 {month_max:,.2f} USD", (timestamps[max_idx], prices[max_idx]),
             textcoords="offset points", xytext=(0, 10), ha='center', color='red', fontsize=9)
plt.annotate(f"底値 {month_min:,.2f} USD", (timestamps[min_idx], prices[min_idx]),
             textcoords="offset points", xytext=(0, -25), ha='center', color='green', fontsize=9)

# 🔽 最大上昇
plt.annotate("",
    xy=(mdates.date2num(timestamps[max_up_idx]), prices[max_up_idx]),
    xytext=(mdates.date2num(timestamps[max_up_idx - 1]), prices[max_up_idx - 1]),
    arrowprops=dict(arrowstyle="<->", color='magenta', lw=2),
)
plt.annotate(f"{max_up_percent:+.2f}%", (timestamps[max_up_idx], prices[max_up_idx]),
             textcoords="offset points", xytext=(0, 12), ha='center', color='magenta', fontsize=9)
plt.annotate(f"▲ +{max_up_val:,.2f} USD", (timestamps[max_up_idx], prices[max_up_idx]),
             textcoords="offset points", xytext=(0, 28), ha='center', color='magenta', fontsize=9)

# 🔽 最大下落
plt.annotate("",
    xy=(mdates.date2num(timestamps[max_down_idx]), prices[max_down_idx]),
    xytext=(mdates.date2num(timestamps[max_down_idx - 1]), prices[max_down_idx - 1]),
    arrowprops=dict(arrowstyle="<->", color='deepskyblue', lw=2),
)
plt.annotate(f"{max_down_percent:+.2f}%", (timestamps[max_down_idx], prices[max_down_idx]),
             textcoords="offset points", xytext=(0, -15), ha='center', color='deepskyblue', fontsize=9)
plt.annotate(f"▼ {max_down_val:,.2f} USD", (timestamps[max_down_idx], prices[max_down_idx]),
             textcoords="offset points", xytext=(0, -32), ha='center', color='deepskyblue', fontsize=9)

# 🔽 凡例
legend_lines = [
    line_main,
    line_dayavg,
    line_avg,
    Line2D([0], [0], color='red', marker='o', linestyle='--', label=f'高値 {month_max:,.2f} USD'),
    Line2D([0], [0], color='green', marker='o', linestyle='--', label=f'底値 {month_min:,.2f} USD'),
    Line2D([0], [0], color='magenta', linestyle='-', label=f'最大上昇: {max_up_label}'),
    Line2D([0], [0], color='deepskyblue', linestyle='-', label=f'最大下落: {max_down_label}')
]
plt.legend(handles=legend_lines, loc=legend_loc, fontsize=9, frameon=True)

# 🔽 軸設定
plt.title(f"BTC月次平均価格（{year}年{month}月）")
plt.xlabel("日付")
plt.ylabel("価格 (USD)")
plt.grid(True)
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.WeekdayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gcf().autofmt_xdate()
plt.tight_layout()

# 🔽 保存
os.makedirs(output_folder, exist_ok=True)
filename = f"btc_monthly_peakdrop_{year}-{month:02d}.png"
output_path = os.path.join(output_folder, filename)
plt.savefig(output_path)
plt.close()
print(f"✅ 月次グラフを保存しました: {output_path}（凡例位置: {legend_loc}）")
