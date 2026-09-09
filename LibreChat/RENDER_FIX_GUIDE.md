# 🚀 LibreChat Render デプロイ - クイック修正ガイド

## ⚠️ 現在のエラー

```
error: Failed to start server: JwtStrategy requires a secret or key
```

## ✅ 修正完了した項目

- [x] `librechat.yaml` ファイルを作成
- [x] JWT シークレットを生成
- [x] 環境変数を `.env` に追加

## 📋 次のステップ (手動で Render ダッシュボードで実施)

### ステップ 1: Render ダッシュボードを開く

**URL**: https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00

### ステップ 2: Environment Variables タブをクリック

左メニューから **"Settings"** > **"Environment"** をクリック

### ステップ 3: 環境変数を追加

以下の環境変数を **Render ダッシュボード** に入力：

| 変数名 | 値 |
|-------|-----|
| `PORT` | `3000` |
| `JWT_SECRET` | `VToW4EL3uaGckdsOX7FR1NZniChBz2mYf8pM6ybvQSUtHI0PlgwJr9K5jexDqA` |
| `JWT_REFRESH_SECRET` | `xY9zAbCdEfGhIjKlMnOpQrStUvWxYzA1bC2dE3fG4hI5jK6lM7nO8pQ9rS0tU1v` |
| `METRICS_SECRET` | `cV6CIkGD3aFEuyZ8ws5vWz0pqftnRJrT` |

**既存の変数は削除しないでください：**
- `MONGODB_URI`
- `DB_NAME`

### ステップ 4: Save ボタンをクリック

変更を保存

### ステップ 5: Manual Deploy

1. Render ダッシュボードで **"Deploy"** ボタンをクリック
2. **"Redeploy latest commit"** を選択
3. デプロイが開始され、ログが表示されます

## 🔍 デプロイ状況を確認

### オプション 1: Render ダッシュボードで確認

https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00

### オプション 2: ローカルから確認

```bash
python retry_deploy.py
```

## 📁 作成されたファイル

| ファイル | 用途 |
|--------|------|
| `librechat.yaml` | LibreChat の設定ファイル |
| `DEPLOYMENT_FIX.md` | 詳細な修正手順 |
| `generate_env.py` | 環境変数生成ツール |
| `.env` | 環境変数（更新済み） |

## 🔐 セキュリティについて

⚠️ **重要**: `.env` ファイルには機密情報が含まれています。

- ✓ `.env` を Git にコミットしないこと
- ✓ GitHub に上げないこと
- ✓ 本番環境では Render ダッシュボードで直接設定すること

## 🆘 トラブルシューティング

### デプロイが失敗する場合

1. **Render のログを確認**
   - ダッシュボード > "Logs" タブで詳細を確認

2. **環境変数が反映されているか確認**
   - Settings > Environment で全て設定されているか確認

3. **librechat.yaml が配置されているか確認**
   - Render の `/app/librechat.yaml` に配置されているか確認

### ポート接続エラーが出る場合

```
Port scan timeout reached, no open ports detected
```

⚠️ `PORT=3000` 環境変数を設定してください

### JWT エラーが出る場合

```
JwtStrategy requires a secret or key
```

⚠️ 以下を確認:
- `JWT_SECRET` が設定されているか
- `JWT_REFRESH_SECRET` が設定されているか
- Render ダッシュボードで "Save" をクリックしたか

## 📞 サポート

- LibreChat 公式: https://www.librechat.ai/
- Render ドキュメント: https://render.com/docs/
- GitHub Issues: https://github.com/danny-avila/LibreChat/issues

---

**最終確認:**

1. [ ] Render ダッシュボードで環境変数を追加した
2. [ ] "Save" をクリックした
3. [ ] "Manual Deploy" で再デプロイした
4. [ ] ログで成功を確認した
5. [ ] https://librechat-9wa4.onrender.com にアクセスできた

**完了後、ここをチェック ✓**
