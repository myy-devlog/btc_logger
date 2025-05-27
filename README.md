# 📈 BTC Logger

CoinbaseのAPIを使って、ビットコイン（BTC）の現在価格を取得し、CSVファイルに自動記録するPythonスクリプトです。

## 🔧 ファイル構成

| ファイル名 | 説明 |
|------------|------|
| `btc_logger.py` | BTC価格を取得してCSVに記録 |
| `Coinbase API.py` | 単発で価格取得して表示するテスト用 |
| `test_connection.py` | ネットワーク接続確認用スクリプト |

## 🛠 使用ライブラリ

- `requests`：API通信
- `datetime`：タイムスタンプ取得
- `csv`：データ保存

## 💡 今後の展望

- 定期実行（タスクスケジューラ連携）
- データ可視化（matplotlib or Webアプリ化）
- DiscordやLINE通知などの応用

---

### 🔹 ② README を Git に追加して Push

```bash
git add README.md
git commit -m "READMEを追加"
git push origin master
