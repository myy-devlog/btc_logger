# 📈 BTC Logger

CoinbaseのAPIを使って、ビットコイン（BTC）の現在価格を取得し、CSVファイルに自動記録するPythonスクリプトです。

---

## 🔧 ファイル構成

| ファイル名            | 説明 |
|-----------------------|------|
| `btc_logger.py`       | BTC価格を取得し、CSVファイルに記録するメインスクリプト |
| `btc_plot.py`         | 直近30件のBTC価格推移を**折れ線グラフ**で可視化するスクリプト【最新版】 |
| `Coinbase API.py`     | 単発でBTC価格を取得し表示するテスト用スクリプト |
| `test_connection.py`  | ネットワーク接続確認用スクリプト |
| `btc_logger.bat`      | タスクスケジューラからPythonスクリプトを実行するためのバッチファイル |

---

## ⚙ 自動実行設定

- Windowsタスクスケジューラを使用して、`btc_logger.bat` を定期的に実行
- 自動的に `btc_log.csv` に価格が追記されます

### ✅ タスクスケジューラ設定手順（Windows）

1. タスクスケジューラを開く
2. 「基本タスクの作成」をクリック
3. 名前を入力（例：btc_logger）
4. トリガー：任意の頻度を選択（例：1時間おき）
5. 操作：「プログラムの開始」を選択し、次を指定：  
   **プログラム/スクリプト**：`btc_logger.bat` のフルパス（例：`C:\Users\Documents\cursor\btc_logger\btc_logger.bat`）
6. 「完了」をクリック
7. 作成したタスクを右クリック → 「プロパティ」 → 「全般」タブ → 「最上位の特権で実行」にチェックを入れる

---

## 📊 グラフ出力機能【NEW】

### btc_plot.py

- `btc_log.csv`の**直近30件のBTC価格推移**を**折れ線グラフ**で可視化し、PNG画像で出力します
- **時系列のズレや重複も自動修正**され、見やすいグラフが生成されます

#### 使い方

1. `btc_logger.py`で自動記録された`btc_log.csv`が存在することを確認
2. 下記コマンドで実行
   ```bash
   python btc_plot.py
3. graphsフォルダ内に「2025-05-XX_line.png」の形式で画像が出力されます

出力サンプル
X軸：日時（直近30件）

Y軸：価格(USD)

青の折れ線：価格の推移

オレンジの点線：平均価格

凡例や日付の見切れも調整済み

🛠 使用ライブラリ
requests：Coinbase APIとの通信

datetime：タイムスタンプ取得

csv：CSV形式でのデータ保存

matplotlib：グラフ描画

🚫 Gitに含まれないファイル
ログファイル btc_log.csv は .gitignore によりGit管理外にしています

生成されるPNG画像も.gitignore対象です

💡 今後の展望（拡張計画）
定期実行の設定（タスクスケジューラ対応）✅

データのグラフ化（matplotlib）✅

Webアプリ化（Flask / Streamlit）

通知機能の追加（LINE / Discord Bot 連携）

週次・月次レポートの自動生成

💻 実行例
bash
コピーする
編集する
$ python btc_logger.py
2025-05-28 10:00:00, 67123.45 USD

$ python btc_plot.py
📊 統計情報（直近30件）
平均価格：102792.77 USD
最高価格：108557.24 USD
最安価格：98359.36 USD
✅ グラフを保存しました: C:/Users/Documents/cursor/btc_logger/graphs/2025-05-29_line.png