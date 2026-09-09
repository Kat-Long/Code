# MongoDB Atlas IP ホワイトリスト設定

## エラー内容

```
Failed to start server: Could not connect to any servers in your MongoDB Atlas cluster.
You're trying to access the database from an IP that isn't whitelisted.
```

## 原因

Render のサーバー IP が MongoDB Atlas のホワイトリストに登録されていません。

## 解決方法

### ステップ 1: MongoDB Atlas にアクセス

1. https://cloud.mongodb.com にアクセス
2. Google アカウントでサインイン

### ステップ 2: Network Access を開く

1. Cluster0 を選択
2. 左メニューから「Security」をクリック
3. 「Network Access」をクリック

### ステップ 3: IP ホワイトリストを設定

#### 方法 1: すべての IP を許可（推奨：開発環境）

1. 「Add IP Address」をクリック
2. 「Allow access from anywhere」を選択
3. IP アドレスに `0.0.0.0/0` が入力される
4. 「Confirm」をクリック

#### 方法 2: 特定の IP のみ許可

1. 「Add IP Address」をクリック
2. IP アドレスに Render サーバー IP を入力
3. 「Confirm」をクリック

**推奨**: 開発環境では 0.0.0.0/0 を使用

### ステップ 4: 設定を確認

1. Network Access でホワイトリストを確認
2. `0.0.0.0/0` が表示されていることを確認

### ステップ 5: デプロイを再試行

Render ダッシュボード（https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00）で：

1. 「Deploys」タブをクリック
2. 最新のデプロイを確認
3. 「Retry」をクリックしてデプロイを再実行

## チェックリスト

- [ ] MongoDB Atlas にアクセス
- [ ] Network Access を開く
- [ ] IP ホワイトリストを設定（0.0.0.0/0）
- [ ] 設定を保存
- [ ] Render デプロイを再試行
- [ ] デプロイが成功するまで待機

## 成功の確認

ログで以下が表示されれば成功：

```
2026-06-14 06:21:38 info: Mongo Connection options
```

その後、サーバーが起動します。

## セキュリティ上の注意

- 開発環境では 0.0.0.0/0 で問題ありません
- 本番環境では特定の IP アドレスのみ許可してください
- IP ホワイトリストは定期的に見直してください