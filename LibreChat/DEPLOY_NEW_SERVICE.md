# Render に LibreChat を再度デプロイする手順

## デプロイ方法

### 方法 1: Render ダッシュボードから手動デプロイ（推奨・簡単）

#### ステップ 1: Render にサインイン
```
https://dashboard.render.com
```

#### ステップ 2: 新しいサービスを作成
1. 「New +」をクリック
2. 「Web Service」を選択

#### ステップ 3: GitHub リポジトリを接続
1. 「Connect a repository」をクリック
2. 「danny-avila/LibreChat」を検索
3. リポジトリを選択

#### ステップ 4: サービス設定
| 設定項目 | 値 |
|---------|-----|
| Name | LibreChat |
| Region | Singapore |
| Branch | main |
| Build Command | （デフォルト） |
| Start Command | npm start |

#### ステップ 5: 環境変数を設定
```
MONGO_URI=mongodb+srv://long1029_db_user:Cfgc5645@cluster0.c5czxzo.mongodb.net/?appName=Cluster0
DB_NAME=librechat
JWT_SECRET=VToW4EL3uaGckdsOX7FR1NZniChBz2mYf8pM6ybvQSUtHI0PlgwJr9K5jexDqA
JWT_REFRESH_SECRET=xY9zAbCdEfGhIjKlMnOpQrStUvWxYzA1bC2dE3fG4hI5jK6lM7nO8pQ9rS0tU1v
METRICS_SECRET=cV6CIkGD3aFEuyZ8ws5vWz0pqftnRJrT
REGISTRATION_ENABLED=true
NODE_ENV=production
```

#### ステップ 6: デプロイ開始
1. 「Create Web Service」をクリック
2. デプロイが開始されます

---

### 方法 2: Render API を使用（プログラム的）

Python スクリプトで自動デプロイ：

```python
import requests
import json

RENDER_API_KEY = "rnd_ABi2u4FwRw68B9newWOeEP01b3zg"
headers = {"Authorization": f"Bearer {RENDER_API_KEY}"}

# サービス作成
service_data = {
    "name": "LibreChat",
    "type": "web_service",
    "repo": "https://github.com/danny-avila/LibreChat",
    "branch": "main",
    "region": "singapore",
    "envVars": [
        {"key": "MONGO_URI", "value": "mongodb+srv://..."},
        {"key": "JWT_SECRET", "value": "..."},
        {"key": "REGISTRATION_ENABLED", "value": "true"},
        # その他の環境変数
    ]
}

response = requests.post(
    "https://api.render.com/v1/services",
    headers=headers,
    json=service_data
)

print(response.json())
```

---

## 環境変数の詳細

### 必須環境変数

| Key | Value | 説明 |
|-----|-------|------|
| MONGO_URI | mongodb+srv://long1029_db_user:Cfgc5645@cluster0.c5czxzo.mongodb.net/?appName=Cluster0 | MongoDB 接続文字列 |
| DB_NAME | librechat | データベース名 |
| JWT_SECRET | VToW4EL3... | JWT 署名用シークレット |
| JWT_REFRESH_SECRET | xY9zAbCd... | リフレッシュトークン用シークレット |

### 推奨環境変数

| Key | Value |
|-----|-------|
| NODE_ENV | production |
| REGISTRATION_ENABLED | true |
| METRICS_SECRET | cV6CIkGD... |
| PORT | 3000 |

---

## デプロイ完了後の確認

### 1. デプロイステータス確認
- Render ダッシュボードで「Live」ステータスを確認

### 2. アプリケーション確認
- https://librechat-[service-id].onrender.com にアクセス

### 3. Sign Up ボタン確認
- ログイン画面に「Sign Up」ボタンが表示されているか確認

### 4. テストログイン
```
Email: admin@example.com
Password: Cfgc5645
```

---

## トラブルシューティング

### デプロイが失敗する場合

1. **ビルドログを確認**
   - Render ダッシュボール → Logs

2. **環境変数を確認**
   - MONGO_URI が正しいか確認
   - すべての JWT シークレットが設定されているか確認

3. **MongoDB 接続確認**
   - MongoDB Atlas の IP ホワイトリスト確認（0.0.0.0/0）

### アプリケーション起動エラー
```
error: JwtStrategy requires a secret or key
```
→ JWT_SECRET が設定されているか確認

```
Failed to connect to MongoDB
```
→ MONGO_URI が正しいか、MongoDB がオンラインか確認

---

## クイックチェックリスト

- [ ] Render ダッシュボールで新しい Web Service を作成
- [ ] GitHub リポジトリを接続
- [ ] すべての環境変数を設定
- [ ] 「Create Web Service」をクリック
- [ ] デプロイ完了を待機（10-15 分）
- [ ] アプリケーション起動を確認
- [ ] Sign Up ボタン表示を確認
- [ ] テストログイン

---

**推奨: Render ダッシュボードから手動で新しいサービスを作成してください！**