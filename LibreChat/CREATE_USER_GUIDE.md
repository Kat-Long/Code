# 🔑 LibreChat ユーザー作成 - 実用ガイド

## Python の問題

環境上で Python が正常に動作していません。以下の代替案を使用してください。

---

## ✅ 代替案 1: Web から Sign Up（最も簡単）

### 推奨: Render で登録機能を有効化

**準備:** Render ダッシュボードで環境変数を設定

1. **URL:** https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00
2. **Settings → Environment**
3. **新しい環境変数を追加:**

```
Key:   REGISTRATION_ENABLED
Value: true
```

4. **Save** をクリック
5. **3-5 分待機** (自動で再デプロイ)
6. **ブラウザをリロード** (Ctrl + F5)
7. **Sign Up** ボタンが表示される

### ユーザー登録フロー

1. https://librechat-9wa4.onrender.com にアクセス
2. **Sign Up** をクリック
3. ユーザー情報を入力：
   ```
   ユーザー名: admin
   メール: admin@example.com
   パスワード: YourSecurePassword123!
   ```
4. **Sign Up** をクリック
5. 登録したユーザーでログイン

---

## ✅ 代替案 2: MongoDB Atlas Web UI で直接作成

### ユーザードキュメントの構造

LibreChat の `users` コレクションに以下の構造でドキュメントを作成：

```json
{
  "username": "admin",
  "email": "admin@example.com",
  "password": "hashed_password",
  "provider": "local",
  "role": "user",
  "verified": true,
  "createdAt": ISODate("2026-06-18T00:00:00.000Z"),
  "updatedAt": ISODate("2026-06-18T00:00:00.000Z"),
  "settings": {}
}
```

### 手動で作成する手順

**ステップ 1: MongoDB Atlas にログイン**

https://cloud.mongodb.com

**ステップ 2: Cluster0 を選択**

**ステップ 3: Collections タブをクリック**

**ステップ 4: librechat > users コレクション**

**ステップ 5: INSERT DOCUMENT をクリック**

**ステップ 6: 以下のドキュメントを入力**

```json
{
  "username": "admin",
  "email": "admin@example.com",
  "password": "$2b$10$...",
  "provider": "local",
  "role": "user",
  "verified": true,
  "createdAt": new Date(),
  "updatedAt": new Date(),
  "settings": {}
}
```

**注意:** パスワードはハッシュ化が必要です。下記の「パスワードハッシュ生成」を参照。

---

## 🔐 パスワードハッシュの生成

LibreChat は bcrypt を使用してパスワードをハッシュ化しています。

### Web ベースのハッシュジェネレータを使用

1. https://bcrypt.online にアクセス
2. パスワードを入力：
   ```
   Password: YourSecurePassword123!
   ```
3. **Hash** をクリック
4. 生成されたハッシュをコピー：
   ```
   $2b$10$...
   ```

### Node.js で生成（開発環境がある場合）

```bash
node -e "require('bcryptjs').hash('YourPassword123!', 10, (err, hash) => console.log(hash))"
```

---

## 📝 完全なユーザー例

### 管理者ユーザーの例

```json
{
  "username": "admin",
  "email": "admin@example.com",
  "password": "$2b$10$NQq3O4xW8pW4N5cJ8m0KQeQ6P1R2S3T4U5V6W7X8Y9Z0A1B2C3D4E5F",
  "provider": "local",
  "role": "user",
  "verified": true,
  "createdAt": new Date("2026-06-18"),
  "updatedAt": new Date("2026-06-18"),
  "settings": {}
}
```

### テストユーザーの例

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "$2b$10$NQq3O4xW8pW4N5cJ8m0KQeQ6P1R2S3T4U5V6W7X8Y9Z0A1B2C3D4E5F",
  "provider": "local",
  "role": "user",
  "verified": true,
  "createdAt": new Date("2026-06-18"),
  "updatedAt": new Date("2026-06-18"),
  "settings": {}
}
```

---

## ✅ 推奨される流れ

### 最も簡単な方法（推奨）

1. **Render で REGISTRATION_ENABLED=true を設定**
2. **5 分待機**
3. **Web から Sign Up で登録**
4. **ログイン**

```
🎯 所要時間: 5-10 分（最も簡単）
```

### バックアップ方法

1. **MongoDB Atlas で直接ユーザーを作成**
2. **ログイン**

```
🎯 所要時間: 10-15 分（手動操作が必要）
```

---

## 🔗 各サービスへのアクセス

| サービス | URL |
|---------|-----|
| **LibreChat** | https://librechat-9wa4.onrender.com |
| **Render ダッシュボード** | https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00 |
| **MongoDB Atlas** | https://cloud.mongodb.com |
| **bcrypt ハッシュジェネレータ** | https://bcrypt.online |

---

## 📋 チェックリスト

### Web Registration を使用する場合

- [ ] Render で REGISTRATION_ENABLED=true を設定した
- [ ] Save をクリックした
- [ ] 5 分待機した
- [ ] ブラウザをリロードした (Ctrl + F5)
- [ ] Sign Up ボタンが表示されているか確認した
- [ ] 新しいユーザーで登録した
- [ ] ログインできた

### MongoDB Atlas で直接作成する場合

- [ ] MongoDB Atlas にログインした
- [ ] librechat > users コレクションを開いた
- [ ] INSERT DOCUMENT をクリックした
- [ ] ユーザードキュメントを入力した
- [ ] パスワードをハッシュ化した
- [ ] INSERT をクリックした
- [ ] LibreChat でログインした

---

## 🆘 トラブルシューティング

### Sign Up ボタンが表示されない

**解決方法:**
1. ブラウザキャッシュをクリア (Ctrl + Shift + Delete)
2. ページをリロード (Ctrl + F5)
3. シークレットモード（プライベートブラウジング）で確認
4. 10 分待機

### ログインできない

**確認事項:**
1. ユーザー名またはパスワードが正確か
2. Caps Lock が ON になっていないか
3. ユーザーが実際に作成されているか（MongoDB で確認）
4. パスワードがハッシュ化されているか

### MongoDB に接続できない

**確認事項:**
1. MongoDB Atlas にログインできるか
2. IP ホワイトリストに 0.0.0.0/0 が追加されているか
3. MONGODB_URI が正しいか

---

## 💡 セキュリティ上の注意

- パスワードは最低 12 文字以上を推奨
- 大文字、小文字、数字、特殊文字を含める
- テスト用パスワードは本番環境では変更する

---

**🎯 推奨: Render で REGISTRATION_ENABLED=true を設定して、Web から Sign Up してください！** 🚀
