# LibreChat JWT シークレット設定ガイド

## エラー内容

```
error: Failed to start server: JwtStrategy requires a secret or key
```

## 原因

LibreChat が JWT シークレットキーを見つけられません。

## 解決方法

### ステップ 1: Render ダッシュボードにアクセス

https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00

### ステップ 2: Environment を開く

1. 左メニューから「Environment」をクリック

### ステップ 3: 環境変数を追加

以下の環境変数を追加してください：

#### 必須環境変数

| Key | Value |
|-----|-------|
| JWT_SECRET | generate-a-secure-random-string-here |
| JWT_REFRESH_SECRET | generate-another-secure-random-string-here |

#### JWT_SECRET の生成方法

Linux/Mac では以下を実行：
```bash
openssl rand -base64 32
```

Windows では Python を使用：
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**例：**
```
JWT_SECRET=gJ7kL9mN2pQrStUvWxYzAbCdEfGhIjKlMnOpQrStUv
JWT_REFRESH_SECRET=aB1cD2eF3gH4iJ5kL6mN7oP8qR9sTuVwXyZ0AbCdEf
```

### ステップ 4: その他の推奨環境変数

| Key | Value |
|-----|-------|
| MONGO_URI | mongodb+srv://long1029_db_user:Cfgc5645@cluster0.c5czxzo.mongodb.net/?appName=Cluster0 |
| DB_NAME | librechat |
| NODE_ENV | production |

### ステップ 5: 設定を保存

1. 「Save」をクリック
2. デプロイが自動的に開始されます

### ステップ 6: デプロイの進行状況を確認

1. 「Deploys」タブをクリック
2. 最新のデプロイのステータスを確認
3. ステータスが「Live」に変わるまで待機

## チェックリスト

- [ ] JWT_SECRET を生成
- [ ] JWT_REFRESH_SECRET を生成
- [ ] 両方の環境変数を Render に設定
- [ ] MONGO_URI が設定されている
- [ ] DB_NAME が設定されている
- [ ] 「Save」をクリック
- [ ] デプロイが完了するまで待機

## 成功の確認

ログで以下が表示されれば成功：

```
2026-06-14 06:41:05 info: Connected to MongoDB
2026-06-14 06:41:11 info: Server started on port 3080
```

その後、https://librechat-9wa4.onrender.com でアクセス可能になります。

## セキュリティ上の注意

- JWT_SECRET は絶対に公開しないでください
- 本番環境では強力なランダム文字列を使用してください
- 定期的にシークレットをローテーションしてください
- .env ファイルは Git にコミットしないでください