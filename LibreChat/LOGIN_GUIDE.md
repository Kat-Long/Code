# LibreChat ログイン情報管理

## 📍 アクセス URL
```
https://librechat-9wa4.onrender.com
```

## ⚙️ 現在の設定状況

| 設定項目 | 状態 |
|---------|------|
| ユーザー登録 | ❌ 無効 (registration.enabled = false) |
| ローカル認証 | ✅ 有効 |
| MongoDB | ✅ 接続済み |
| JWT 認証 | ✅ 設定済み |

## 🔐 ログイン情報管理方法

### オプション 1: ユーザー管理スクリプトで管理（推奨）

```bash
python user_management.py
```

このスクリプトで以下が可能：
- ✅ ユーザーを作成
- ✅ ユーザー一覧を表示
- ✅ ユーザーを削除
- ✅ パスワードをハッシュ化して保存

### オプション 2: 登録を有効にする（自由登録）

`librechat.yaml` の設定を変更：

```yaml
registration:
  enabled: true  # false から true に変更
```

その後、Render にデプロイし直すと、ユーザーが自由に登録できるようになります。

### オプション 3: MongoDB Atlas でユーザーを直接操作

MongoDB Atlas の Web UI から直接ユーザーを管理することも可能。

---

## 📝 ユーザー作成手順

### ステップ 1: ユーザー管理スクリプトを実行

```bash
cd "c:\Users\long\OneDrive\Code\LibreChat"
python user_management.py
```

### ステップ 2: メニューから「1. ユーザーを作成」を選択

```
操作を選択:
  1. ユーザーを作成
  2. ユーザー一覧を表示
  3. ユーザーを削除
  4. 終了

選択 (1-4): 1
```

### ステップ 3: ユーザー情報を入力

```
ユーザー名を入力: admin
メールアドレスを入力: admin@example.com
パスワードを入力: securepassword123
```

### ステップ 4: 作成完了

```
[SUCCESS] ユーザーを作成しました！
  ログイン URL: https://librechat-9wa4.onrender.com
  ユーザー名: admin
  パスワード: ****
```

---

## 🔍 ユーザー一覧の確認

メニューから「2. ユーザー一覧を表示」を選択すると、登録済みユーザーが表示されます：

```
[OK] 登録済みユーザー (2 件):

  - ユーザー名: admin
    Email: admin@example.com
    ロール: user
    作成日: 2026-06-18 12:34:56.789000

  - ユーザー名: user1
    Email: user1@example.com
    ロール: user
    作成日: 2026-06-18 12:35:00.000000
```

---

## 🗑️ ユーザーの削除

メニューから「3. ユーザーを削除」を選択します：

```
削除するユーザー名を入力: user1
[OK] ユーザー 'user1' を削除しました
```

---

## 🔑 パスワードリセット

LibreChat では、初期状態ではパスワードリセット機能が実装されていません。

**パスワードをリセットするには：**

1. ユーザー管理スクリプトでユーザーを削除
2. 新しいパスワードで再作成
3. または MongoDB で直接パスワードを更新

### MongoDB での直接更新方法

MongoDB Atlas Web UI で、`users` コレクション内のユーザードキュメントのパスワード フィールドを更新します。

---

## 📊 デフォルトユーザー設定

スクリプトで作成されたユーザーのデフォルト設定：

```javascript
{
  "username": "username",
  "email": "user@example.com",
  "password": "hashed_password",
  "provider": "local",
  "role": "user",          // 一般ユーザー（admin にするには手動で変更必要）
  "verified": true,        // メール認証済み
  "settings": {}
}
```

---

## ⚠️ セキュリティに関する注意

1. **強力なパスワードを使用**
   - 最低 12 文字以上
   - 大文字、小文字、数字、特殊文字を含める

2. **.env ファイルを保護**
   - Git にコミットしない
   - AWS Secrets Manager や環境変数として管理

3. **HTTPS を使用**
   - Render は自動的に HTTPS を有効化
   - 常に HTTPS でアクセス

4. **JWT シークレットを定期的に更新**
   - 3〜6 ヶ月ごとに更新推奨

---

## 🐛 トラブルシューティング

### MongoDB 接続エラーが出る

```
[ERROR] MongoDB 接続失敗: ...
```

**解決方法:**
- `.env` ファイルで `MONGODB_URI` を確認
- MongoDB Atlas で IP ホワイトリストを確認（0.0.0.0/0 に設定）
- インターネット接続を確認

### ユーザーが既に存在するエラー

```
[ERROR] ユーザー 'admin' は既に存在します
```

**解決方法:**
- 異なるユーザー名を使用
- または既存ユーザーを削除してから作成

### ログインできない

```
ユーザー名またはパスワードが正しくありません
```

**確認事項:**
- ユーザー名とパスワードが正確に入力されているか
- Caps Lock が有効になっていないか
- ユーザーが実際に作成されているか（リスト表示で確認）

---

## 💡 ヒント

### 管理者ユーザーを最初に作成

```bash
python user_management.py
# 1. ユーザー作成
# ユーザー名: admin
# メール: admin@example.com
# パスワード: [強力なパスワード]
```

### テストユーザーを複数作成

```bash
# ユーザー1
# ユーザー名: testuser1
# メール: test1@example.com
# パスワード: testpass123

# ユーザー2
# ユーザー名: testuser2
# メール: test2@example.com
# パスワード: testpass456
```

---

## 📞 参考リンク

- LibreChat 公式: https://www.librechat.ai/
- MongoDB ドキュメント: https://docs.mongodb.com/
- Render ダッシュボード: https://dashboard.render.com/
