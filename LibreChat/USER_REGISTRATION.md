# LibreChat ユーザー登録設定ガイド

## 📝 ユーザー登録の有効化

LibreChat で Web サイトから直接ユーザー登録できるようにしました。

## ✅ 現在の設定

```yaml
registration:
  enabled: true
  requireEmail: false        # メール認証なしで登録可能
  allowMultipleAccounts: true # 複数アカウント作成を許可
```

| 設定項目 | 値 | 説明 |
|---------|-----|------|
| `enabled` | `true` | ユーザー登録機能を有効化 |
| `requireEmail` | `false` | メール認証なしで登録可能 |
| `allowMultipleAccounts` | `true` | 1 人が複数のアカウントを作成可能 |

---

## 🌐 Web からのユーザー登録方法

### ステップ 1: サイトにアクセス

```
https://librechat-9wa4.onrender.com
```

### ステップ 2: 「Sign Up」または「Create Account」をクリック

ログイン画面で「Sign Up」ボタンを探してクリック

### ステップ 3: 登録フォームに入力

以下の情報を入力：

```
ユーザー名: [任意のユーザー名]
メール: [メールアドレス（任意）]
パスワード: [12文字以上を推奨]
パスワード確認: [上記と同じ]
```

### ステップ 4: 「Sign Up」または「Register」をクリック

登録が完了します

### ステップ 5: ログイン

登録されたユーザー名とパスワードでログイン

---

## 🔐 登録前に Render にデプロイ

**重要**: 変更を Render に反映させるには、再デプロイが必要です。

### ステップ 1: Render ダッシュボードを開く

```
https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00
```

### ステップ 2: Deploy をクリック

**Methods:**

#### 方法 A: 自動デプロイ（Git 連携の場合）

```bash
git add librechat.yaml
git commit -m "Enable user registration"
git push origin main
```

#### 方法 B: 手動デプロイ

1. Render ダッシュボードで **"Manual Deploy"** をクリック
2. **"Redeploy latest commit"** を選択
3. デプロイが開始されます

#### 方法 C: Render API 経由

```bash
python retry_deploy.py
```

### ステップ 3: デプロイ完了を待つ

Render のログで「Deploy successful」を確認

---

## 📊 設定の詳細説明

### `enabled: true`
- ユーザー登録ページが表示される
- Web UI に「Sign Up」ボタンが出現

### `requireEmail: false`
- メール検証をスキップ
- 即座にアカウントが有効化される
- スパム対策が必要な場合は `true` に設定

### `allowMultipleAccounts: true`
- 1 人で複数のアカウントを作成可能
- 複数プロジェクト用途に便利
- 制限したい場合は `false` に設定

---

## ⚙️ オプション設定

### メール認証を有効にする

```yaml
registration:
  enabled: true
  requireEmail: true         # メール認証を必須化
  allowMultipleAccounts: true
```

変更後、ユーザーは登録時にメール確認リンクをクリックする必要があります。

### 複数アカウント作成を禁止

```yaml
registration:
  enabled: true
  requireEmail: false
  allowMultipleAccounts: false  # 1 ユーザー = 1 アカウント
```

### 登録を再び無効化

```yaml
registration:
  enabled: false  # false に戻すと登録ページが非表示
```

---

## 🔍 登録確認方法

### Web UI での確認

1. 新しいユーザーで登録
2. 登録したユーザー名でログイン
3. ダッシュボードが表示されば成功

### Python スクリプトでの確認

```bash
python user_management.py
# 選択: 2
# → 登録されたユーザーが表示される
```

---

## ⚠️ セキュリティに関する注意

### 登録を有効化する際の注意点

| 項目 | リスク | 対策 |
|------|------|------|
| スパム登録 | 大量の架空アカウント | レート制限を設定 |
| 弱いパスワード | セキュリティリスク | 最小文字数を設定 |
| メール検証なし | 無効なメールアドレス | メール認証を有効化 |

### 推奨設定

```yaml
registration:
  enabled: true
  requireEmail: true         # メール認証を有効化
  allowMultipleAccounts: false # 1 ユーザー = 1 アカウント
```

---

## 📝 ユーザー登録後の管理

### 登録済みユーザーの確認

```bash
python user_management.py
# 選択: 2
```

### ユーザーの削除

```bash
python user_management.py
# 選択: 3
```

### ユーザーのロール変更

MongoDB Atlas で直接 `role` フィールドを編集：
- `user` - 一般ユーザー
- `admin` - 管理者

---

## 🔗 関連ドキュメント

- `LOGIN_GUIDE.md` - ログイン管理の詳細
- `user_management.py` - ユーザー管理スクリプト
- `RENDER_FIX_GUIDE.md` - Render デプロイ手順
- `librechat.yaml` - 設定ファイル

---

## 📞 トラブルシューティング

### 「Sign Up」ボタンが表示されない

**原因:** 設定が Render に反映されていない

**解決方法:**
1. `librechat.yaml` で `registration.enabled = true` を確認
2. Render で "Manual Deploy" を実行
3. ブラウザをリロード

### 登録ができない

**原因:** サーバーエラーまたは設定ミス

**解決方法:**
1. Render のログを確認
2. MongoDB 接続を確認
3. JWT シークレットが設定されているか確認

### 登録後にログインできない

**原因:** アカウントの同期遅延

**解決方法:**
1. 5 分待機
2. ページをリロード
3. シークレットモード（プライベートブラウジング）で試行

---

## 🎯 推奨される次のステップ

### ステップ 1: 設定変更を Render にデプロイ

```bash
# 自動デプロイ（Git 連携）
git add librechat.yaml
git commit -m "Enable user registration"
git push

# または手動デプロイ
python retry_deploy.py
```

### ステップ 2: デプロイ完了を確認

Render ダッシュボードで「Deploy successful」を確認

### ステップ 3: 新しいユーザーで登録テスト

```
https://librechat-9wa4.onrender.com → Sign Up
```

### ステップ 4: 登録成功を確認

登録したユーザーでログインできることを確認

---

**✅ 準備完了！Render にデプロイしてから、Web サイトからユーザー登録をお試しください。** 🚀
