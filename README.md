# 📈 BTC Logger

CoinbaseのAPIを使って、ビットコイン（BTC）の現在価格を取得し、CSVファイルに自動記録するPythonスクリプトです。

---

## 🔧 ファイル構成

| ファイル名                  | 説明 |
|-----------------------------|------|
| `btc_logger.py`             | BTC価格を取得し、CSVファイルに記録するメインスクリプト |
| `btc_plot.py`               | 直近30件のBTC価格推移を折れ線グラフで可視化するスクリプト |
| `btc_oneday_peakdrop.py`    | 指定日（0:00〜0:00）の価格変動をグラフ化（日次レポート）|
| `btc_weekly_peakdrop.py`    | 週次で最大上昇・下落を含む比較グラフを作成（週次レポート）|
| `btc_monthly_peakdrop.py`   | 月次で最大・最小を含む集計グラフを作成（月次レポート）|
| `btc_binance_month_data.py` | Binance APIから月次データを取得しCSVに保存 |
| `Coinbase API.py`           | 単発でBTC価格を取得し表示するテスト用スクリプト |
| `test_connection.py`        | ネットワーク接続確認用スクリプト |
| `btc_logger.bat`            | タスクスケジューラからスクリプトを実行するバッチファイル |

---

## ⚙ 自動実行設定（btc_logger.py）

- Windowsタスクスケジューラを使って `btc_logger.bat` を定期実行
- 自動で `btc_log.csv` に価格を記録

---

## 📊 可視化・レポート出力機能

### 📅 日次レポート（btc_oneday_peakdrop.py）
- 指定した1日（JST 0:00〜0:00）を対象に価格推移をグラフ化
- 高値・底値、最大上昇・下落を色分け表示

### 📈 週次レポート（btc_weekly_peakdrop.py）
- 今週と先週の日別価格を比較
- 週ごとの平均・中央値・最大上下動をプロット

### 📆 月次レポート（btc_monthly_peakdrop.py）
- 月単位での平均・高値・底値をバーグラフで出力
- Binanceの履歴データを活用

---

## 🖼 グラフ例（btc_plot.py）

- `btc_log.csv` の直近30件のデータを可視化
- 平均価格とともに時系列プロット
- 自動で `graphs/` フォルダにPNG形式で保存

---

## 🔄 最新アップデート情報

- `2025-06-01`: 日次/週次/月次レポートスクリプトを追加
- 詳細は [CHANGELOG.md](./CHANGELOG.md) を参照

---

## 💡 今後の展望

- Webアプリ化（Flask / Streamlit）
- 通知機能（LINE / Discord）
- トークン価格比較・マルチコイン対応

---

## 🛠 使用ライブラリ

- `requests`：API通信
- `csv`：ログ保存
- `datetime`：タイムスタンプ処理
- `matplotlib`：可視化
- `zoneinfo`：JST変換（Python 3.9+）

---

## 🚫 Git管理外ファイル

- `btc_log.csv` や `graphs/*.png` は `.gitignore` によりGit管理外

---

## 💻 実行例

```bash
$ python btc_logger.py
2025-06-01 09:00:00, 67200.00 USD

$ python btc_oneday_peakdrop.py
📊 最高: 67,500 USD | 最安: 66,400 USD | 平均: 66,950 USD
✅ グラフ保存: graphs/oneday_2025-06-01_peakdrop.png
```
