# 📈 BTC Logger

CoinbaseのAPIを使って、ビットコイン（BTC）の現在価格を取得し、CSVファイルに自動記録するPythonスクリプトです。

## 🔧 ファイル構成

| ファイル名            | 説明 |
|-----------------------|------|
| `btc_logger.py`       | BTC価格を取得し、CSVファイルに記録するメインスクリプト |
| `Coinbase API.py`     | 単発でBTC価格を取得し表示するテスト用スクリプト |
| `test_connection.py`  | ネットワーク接続確認用スクリプト |
| `btc_logger.bat`      | タスクスケジューラからPythonスクリプトを実行するためのバッチファイル |

## ⚙ 自動実行設定

- Windowsタスクスケジューラを使用して、`btc_logger.bat` を定期的に実行
- 自動的に `btc_log.csv` に価格が追記されます

### ✅ タスクスケジューラ設定手順（Windows）

1. タスクスケジューラを開く
2. 「基本タスクの作成」をクリック
3. 名前を入力（例：btc_logger）
4. トリガー：任意の頻度を選択（例：1時間おき）
5. 操作：「プログラムの開始」を選択し、次を指定：
   - **プログラム/スクリプト**：`btc_logger.bat` のフルパス（例：`C:\Users\Mizuki\Documents\cursor\btc_logger\btc_logger.bat`）
6. 「完了」をクリック
7. 作成したタスクを右クリック → 「プロパティ」 → 「全般」タブ → 「最上位の特権で実行」にチェックを入れる

## 🛠 使用ライブラリ

- `requests`：Coinbase APIとの通信
- `datetime`：タイムスタンプ取得
- `csv`：CSV形式でのデータ保存

## 🚫 Gitに含まれないファイル

- ログファイル `btc_log.csv` は `.gitignore` によりGit管理外にしています

## 💡 今後の展望（拡張計画）

- 定期実行の設定（タスクスケジューラ対応）✅
- データのグラフ化（matplotlib）
- Webアプリ化（Flask / Streamlit）
- 通知機能の追加（LINE / Discord Bot 連携）

---

## 💻 実行例

```bash
$ python btc_logger.py
2025-05-28 10:00:00, 67123.45 USD
