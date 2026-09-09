# LibreChat ログイン情報 - クイックガイド

## 🌐 アクセス URL
```
https://librechat-9wa4.onrender.com
```

## 📋 現在のステータス

| 項目 | ステータス |
|------|-----------|
| サービス | 🔧 デプロイ中（修正設定待ち） |
| ユーザー登録 | ❌ 無効 |
| 認証方式 | JWT (ローカル認証) |
| DB | MongoDB |

## ✅ ユーザーの作成方法

### 方法 1: ユーザー管理スクリプト（推奨）

ファイル: `user_management.py`

**使用方法:**
```bash
python user_management.py
```

**メニュー:**
```
1. ユーザーを作成
2. ユーザー一覧を表示
3. ユーザーを削除
4. 終了
```

**例: admin ユーザー作成**
```
選択: 1
ユーザー名: admin
メール: admin@example.com
パスワード: YourSecurePassword123!
```

### 方法 2: 登録を有効にする

`librechat.yaml` で以下を変更：

```yaml
# 変更前
registration:
  enabled: false

# 変更後
registration:
  enabled: true
```

その後、Render で再デプロイすると、Web UI から自由にユーザー登録できます。

### 方法 3: MongoDB 直接操作

MongoDB Atlas Web UI から `users` コレクションに直接ドキュメントを挿入。

---

## 🔐 推奨されるデフォルトユーザー設定

**初期管理者ユーザー:**
```
ユーザー名: admin
メール: your-email@example.com
パスワード: [強力なパスワード 12文字以上]
```

**テストユーザー:**
```
ユーザー名: demo
メール: demo@example.com
パスワード: demo123456
```

---

## 📝 ログイン画面での入力

サイトにアクセスして「Login」をクリック：

```
Username/Email: [上記で作成したユーザー名またはメール]
Password: [設定したパスワード]
```

---

## ⚙️ 必要な次のステップ

### 1️⃣ Render ダッシュボードで環境変数を設定
https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00

→ `RENDER_FIX_GUIDE.md` を参照

### 2️⃣ 再デプロイを実行
Render ダッシュボードで "Manual Deploy" をクリック

### 3️⃣ サイトが起動したら、ユーザーを作成
```bash
python user_management.py
```

### 4️⃣ 作成したユーザーでログイン
https://librechat-9wa4.onrender.com

---

## 🆘 トラブルシューティング

| 問題 | 原因 | 解決方法 |
|------|------|---------|
| ログイン画面が表示されない | Render デプロイ失敗 | `RENDER_FIX_GUIDE.md` を確認 |
| ユーザーが作成できない | MongoDB 未接続 | `.env` ファイルの `MONGODB_URI` を確認 |
| ログインできない | ユーザー未作成 | `python user_management.py` で作成 |
| パスワードを忘れた | ユーザー削除・再作成 | `python user_management.py` で削除後に再作成 |

---

## 📚 関連ドキュメント

- `LOGIN_GUIDE.md` - 詳細なログイン管理ガイド
- `RENDER_FIX_GUIDE.md` - Render デプロイ修正手順
- `DEPLOYMENT_FIX.md` - デプロイの詳細トラブルシューティング
- `user_management.py` - ユーザー管理スクリプト

---

## 🔗 デフォルトログイン情報

**初回ログイン後に変更してください！**

初期テスト用（ユーザー管理スクリプトで作成）:
```
ユーザー名: test
メール: test@librechat.local
パスワード: test12345
```

---

**すぐに実行:**
1. `RENDER_FIX_GUIDE.md` に従い、Render で環境変数を設定
2. `python user_management.py` でユーザーを作成
3. https://librechat-9wa4.onrender.com でログイン
