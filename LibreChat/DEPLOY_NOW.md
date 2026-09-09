# 🚀 Render デプロイ - クイックスタート

## 📝 変更内容

`librechat.yaml` でユーザー登録を有効化しました：

```yaml
registration:
  enabled: true              # ✅ ユーザー登録を有効化
  requireEmail: false        # メール認証なしで登録可能
  allowMultipleAccounts: true # 複数アカウント作成を許可
```

---

## 🚀 Render にデプロイする方法

### 方法 A: Python スクリプトで再デプロイ（推奨）

```bash
cd "c:\Users\long\OneDrive\Code\LibreChat"
python retry_deploy.py
```

### 方法 B: Render ダッシュボードで手動デプロイ

1. https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00 を開く
2. **"Redeploy latest commit"** をクリック
3. デプロイ完了を待つ

### 方法 C: Git で自動デプロイ（連携している場合）

```bash
git add librechat.yaml
git commit -m "Enable user registration on LibreChat"
git push origin main
```

---

## ⏱️ デプロイ時間

通常 5〜10 分で完了します

**進捗確認:**
- Render ダッシュボードの「Logs」タブ
- または Render からのメール通知

---

## ✅ デプロイ完了後

### ステップ 1: サイトにアクセス

```
https://librechat-9wa4.onrender.com
```

### ステップ 2: 「Sign Up」をクリック

ログイン画面に「Sign Up」ボタンが表示されます

### ステップ 3: 新規ユーザーで登録

```
ユーザー名: testuser
メール: test@example.com
パスワード: TestPassword123!
```

### ステップ 4: ログイン

登録したユーザーでログイン可能

---

## 🔍 デプロイ状況の確認

### リアルタイムログを確認

Render ダッシュボード → **Logs** タブで：

```
==> Deploying...
==> Setting WEB_CONCURRENCY=1...
...
==> Build successful
==> Starting service
==> Service started successfully
```

### スクリプトでの確認

```bash
python librechat_render.py
```

---

## ⚠️ よくある問題と解決策

| 問題 | 原因 | 解決方法 |
|------|------|---------|
| Sign Up が表示されない | デプロイ未完了 | ブラウザをリロード / 5 分待機 |
| 登録がエラーになる | MongoDB 未接続 | Render ログを確認 |
| パスワード要件エラー | 弱いパスワード | 12文字以上＆大文字含める |

---

## 📋 チェックリスト

- [ ] `librechat.yaml` で `registration.enabled = true` を確認
- [ ] Render にデプロイを実行
- [ ] デプロイ完了を確認
- [ ] https://librechat-9wa4.onrender.com にアクセス
- [ ] 「Sign Up」ボタンが表示されているか確認
- [ ] 新しいユーザーで登録をテスト
- [ ] ログイン成功を確認

---

## 💡 その他のオプション

### メール認証を有効化（スパム対策）

```yaml
registration:
  enabled: true
  requireEmail: true  # true に変更
```

### 複数アカウント作成を禁止

```yaml
registration:
  enabled: true
  allowMultipleAccounts: false  # false に変更
```

---

## 🔗 関連リンク

- LibreChat 設定: `USER_REGISTRATION.md`
- ユーザー管理スクリプト: `user_management.py`
- Render ダッシュボード: https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00
- LibreChat 公式: https://www.librechat.ai/

---

**今すぐデプロイを開始！** 🚀

```bash
python retry_deploy.py
```
