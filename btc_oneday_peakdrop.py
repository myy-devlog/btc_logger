import csv
from datetime import datetime, timedelta, time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import numpy as np
from matplotlib.lines import Line2D
from zoneinfo import ZoneInfo

# ====== 設定 ======
csv_path = r"C:/Users/Mizuki/Documents/cursor/btc_logger/btc_log.csv"
output_folder = r"C:/Users/Mizuki/Documents/cursor/btc_logger/graphs"
plt.rcParams['font.family'] = 'Meiryo'
jst = ZoneInfo("Asia/Tokyo")

# ====== 日付入力 ======
input_str = input("📅 日付を入力してください（例: 2025-06-01、未入力で過去24時間）: ").strip()
if input_str:
    try:
        target_day = datetime.strptime(input_str, "%Y-%m-%d").date()
        start_dt = datetime.combine(target_day, time(0, 0)).replace(tzinfo=jst)
        end_dt = start_dt + timedelta(days=1)
        title_day = target_day
    except:
        print("❌ 日付形式が正しくありません。例: 2025-06-01")
        exit()
else:
    now = datetime.now(jst)
    end_dt = now.replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
    start_dt = end_dt - timedelta(hours=24)
    title_day = start_dt.date()

# ====== データ読み込み（0:00〜24:00） ======
timestamps, prices = [], []
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            t = datetime.fromisoformat(row[0]).astimezone(jst)
            if start_dt <= t < end_dt:
                timestamps.append(t)
                prices.append(float(row[1]))
        except:
            continue

if not prices:
    print("❌ 指定された期間にデータがありません。")
    print(f"⏱ 期間: {start_dt} ～ {end_dt}")
    exit()

# ====== 指標計算 ======
avg_price = np.mean(prices)
max_price = np.max(prices)
min_price = np.min(prices)
max_idx = np.argmax(prices)
min_idx = np.argmin(prices)

price_diffs = np.diff(prices)
max_up_idx = np.argmax(price_diffs) + 1
max_down_idx = np.argmin(price_diffs) + 1
max_up_val = price_diffs[max_up_idx - 1]
max_down_val = price_diffs[max_down_idx - 1]
max_up_percent = (max_up_val / prices[max_up_idx - 1]) * 100 if prices[max_up_idx - 1] != 0 else 0
max_down_percent = (max_down_val / prices[max_down_idx - 1]) * 100 if prices[max_down_idx - 1] != 0 else 0

# ====== グラフ描画 ======
fig, ax = plt.subplots(figsize=(12, 6))
line_main, = ax.plot(timestamps, prices, marker='o', color='dodgerblue', label="価格")
line_avg = ax.axhline(y=avg_price, color='orange', linestyle='--', label=f'平均 {avg_price:,.2f} USD')
ax.axhline(y=max_price, color='red', linestyle='--', linewidth=1)
ax.axhline(y=min_price, color='green', linestyle='--', linewidth=1)

# 高値・底値 注釈
ax.scatter([timestamps[max_idx]], [max_price], color='red', zorder=5)
ax.annotate(f"高値 {max_price:,.2f} USD", (timestamps[max_idx], max_price),
            textcoords="offset points", xytext=(0, 10), ha='center', color='red', fontsize=10)

ax.scatter([timestamps[min_idx]], [min_price], color='green', zorder=5)
ax.annotate(f"底値 {min_price:,.2f} USD", (timestamps[min_idx], min_price),
            textcoords="offset points", xytext=(0, -20), ha='center', color='green', fontsize=10)

# 最大上昇
ax.plot([timestamps[max_up_idx - 1], timestamps[max_up_idx]],
        [prices[max_up_idx - 1], prices[max_up_idx]], color='magenta', linewidth=2)
ax.scatter([timestamps[max_up_idx - 1], timestamps[max_up_idx]],
           [prices[max_up_idx - 1], prices[max_up_idx]], color='magenta', zorder=6)
ax.annotate(f"{max_up_percent:+.2f}%", (timestamps[max_up_idx], prices[max_up_idx]),
            textcoords="offset points", xytext=(0, 10), ha='center', color='magenta', fontsize=9)
ax.annotate(f"▲+{max_up_val:,.2f} USD", (timestamps[max_up_idx], prices[max_up_idx]),
            textcoords="offset points", xytext=(0, 26), ha='center', color='magenta', fontsize=9)

# 最大下落
ax.plot([timestamps[max_down_idx - 1], timestamps[max_down_idx]],
        [prices[max_down_idx - 1], prices[max_down_idx]], color='deepskyblue', linewidth=2)
ax.scatter([timestamps[max_down_idx - 1], timestamps[max_down_idx]],
           [prices[max_down_idx - 1], prices[max_down_idx]], color='deepskyblue', zorder=6)
ax.annotate(f"{max_down_percent:+.2f}%", (timestamps[max_down_idx], prices[max_down_idx]),
            textcoords="offset points", xytext=(0, -30), ha='center', color='deepskyblue', fontsize=9)
ax.annotate(f"▼{abs(max_down_val):,.2f} USD", (timestamps[max_down_idx], prices[max_down_idx]),
            textcoords="offset points", xytext=(0, -46), ha='center', color='deepskyblue', fontsize=9)

# 凡例（最大上昇・下落の詳細表示）
legend_lines = [
    line_main,
    line_avg,
    Line2D([0], [0], color='red', marker='o', linestyle='--', label=f'高値 {max_price:,.2f} USD'),
    Line2D([0], [0], color='green', marker='o', linestyle='--', label=f'底値 {min_price:,.2f} USD'),
    Line2D([0], [0], color='magenta', linestyle='-', label=(
        f"最大上昇: {timestamps[max_up_idx - 1].strftime('%Y-%m-%d %H:%M')}～{timestamps[max_up_idx].strftime('%H:%M')} (JST)  "
        f"{prices[max_up_idx - 1]:,.2f}→{prices[max_up_idx]:,.2f} "
        f"({max_up_percent:+.2f}%)")),
    Line2D([0], [0], color='deepskyblue', linestyle='-', label=(
        f"最大下落: {timestamps[max_down_idx - 1].strftime('%Y-%m-%d %H:%M')}～{timestamps[max_down_idx].strftime('%H:%M')} (JST)  "
        f"{prices[max_down_idx - 1]:,.2f}→{prices[max_down_idx]:,.2f} "
        f"({max_down_percent:+.2f}%)"))
]
ax.legend(handles=legend_lines, loc='best', fontsize=9)

# ====== X軸設定：23:00〜翌01:00（±1時間表示） ======
x_axis_min = datetime.combine(title_day, time(0, 0)).replace(tzinfo=jst) - timedelta(hours=1)
x_axis_max = datetime.combine(title_day, time(0, 0)).replace(tzinfo=jst) + timedelta(hours=25)
ax.set_xlim([x_axis_min, x_axis_max])
ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M', tz=jst))
plt.xticks(rotation=45)

# ====== その他設定 ======
ax.set_title(f"BTC価格の推移（{title_day}）")
ax.set_xlabel("時刻（JST）")
ax.set_ylabel("価格 (USD)")
ax.grid(True)
plt.tight_layout()

# ====== 保存 ======
os.makedirs(output_folder, exist_ok=True)
filename = f"oneday_{title_day.strftime('%Y-%m-%d')}_peakdrop.png"
output_path = os.path.join(output_folder, filename)
plt.savefig(output_path)
plt.close()

print(f"✅ {title_day}のグラフを保存しました: {output_path}")
