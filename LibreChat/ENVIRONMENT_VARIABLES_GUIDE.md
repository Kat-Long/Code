# 🔧 Render Environment Variables - 完全ガイド

## 📍 アクセス方法

### ステップ 1: Render ダッシュボードにアクセス
```
https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00
```

### ステップ 2: Settings タブをクリック
- 左側のサイドバーで **Settings** を探してクリック
- または、ページ上部のメニューから **Settings** を選択

### ステップ 3: Environment セクションを探す
- Settings ページ内で **Environment** セクションを見つけてクリック
- または、直接このリンクで開く：
  ```
  https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00/settings
  ```

---

## 🔑 必須の環境変数

### 現在設定すべき変数

| キー | 値 | 説明 |
|------|-----|------|
| `REGISTRATION_ENABLED` | `true` | **【最重要】** Sign Up ボタンを表示 |
| `JWT_SECRET` | `VToW4EL3uaGckdsOX7FR1NZniChBz2mYf8pM6ybvQSUtHI0PlgwJr9K5jexDqA` | JWT 認証用シークレット |
| `JWT_REFRESH_SECRET` | `xY9zAbCdEfGhIjKlMnOpQrStUvWxYzA1bC2dE3fG4hI5jK6lM7nO8pQ9rS0tU1v` | リフレッシュトークン用 |
| `MONGODB_URI` | `mongodb+srv://long1029_db_user:Cfgc5645@cluster0.c5czxzo.mongodb.net/?appName=Cluster0` | MongoDB 接続文字列 |
| `DB_NAME` | `librechat` | データベース名 |
| `PORT` | `3000` | アプリケーション起動ポート |
| `METRICS_SECRET` | `cV6CIkGD3aFEuyZ8ws5vWz0pqftnRJrT` | メトリクス用シークレット |

---

## ➕ 環境変数を追加する手順

### 方法 1: UI で追加（推奨）

1. **Settings → Environment** を開く
2. **+ Add Environment Variable** ボタンをクリック
3. 以下を入力：
   - **Key**: `REGISTRATION_ENABLED`
   - **Value**: `true`
4. **Save** または **Add** をクリック
5. **Deploy changes** をクリック

### 方法 2: 一括で設定

以下を順番に追加してください：

#### 追加 1: REGISTRATION_ENABLED
```
Key: REGISTRATION_ENABLED
Value: true
```

#### 追加 2: JWT_SECRET
```
Key: JWT_SECRET
Value: VToW4EL3uaGckdsOX7FR1NZniChBz2mYf8pM6ybvQSUtHI0PlgwJr9K5jexDqA
```

#### 追加 3: JWT_REFRESH_SECRET
```
Key: JWT_REFRESH_SECRET
Value: xY9zAbCdEfGhIjKlMnOpQrStUvWxYzA1bC2dE3fG4hI5jK6lM7nO8pQ9rS0tU1v
```

#### 追加 4: MONGODB_URI
```
Key: MONGODB_URI
Value: mongodb+srv://long1029_db_user:Cfgc5645@cluster0.c5czxzo.mongodb.net/?appName=Cluster0
```

#### 追加 5: DB_NAME
```
Key: DB_NAME
Value: librechat
```

#### 追加 6: PORT
```
Key: PORT
Value: 3000
```

#### 追加 7: METRICS_SECRET
```
Key: METRICS_SECRET
Value: cV6CIkGD3aFEuyZ8ws5vWz0pqftnRJrT
```

---

## ✅ 確認手順

### ステップ 1: 全変数が追加されたか確認
Environment セクションで以下が表示されているか確認：
- [ ] REGISTRATION_ENABLED
- [ ] JWT_SECRET
- [ ] JWT_REFRESH_SECRET
- [ ] MONGODB_URI
- [ ] DB_NAME
- [ ] PORT
- [ ] METRICS_SECRET

### ステップ 2: Save & Deploy
1. すべての変数を追加したら、**Save Changes** をクリック
2. **Deploy** または **Redeploy** をクリック
3. Logs タブで「Your service is live 🎉」を確認するまで待機（5-10 分）

### ステップ 3: 機能確認
デプロイ完了後：
```
https://librechat-9wa4.onrender.com
```

1. ブラウザをリロード（Ctrl + F5）
2. **「Sign Up」ボタンが表示されているか確認**
3. 表示されていれば設定成功 ✓

---

## 🔍 トラブルシューティング

### Q: 環境変数が保存されない
**A**: 
- 各変数の後で **Save** をクリックしているか確認
- ページを再読込してから確認
- ブラウザのデベロッパーツール（F12）でコンソールエラーを確認

### Q: Sign Up ボタンがまだ表示されない
**A**:
- REGISTRATION_ENABLED = true が設定されているか確認
- Logs で再デプロイが完了しているか確認（「Your service is live」）
- ブラウザキャッシュをクリア：Ctrl + Shift + Delete
- ハード リロード：Ctrl + F5

### Q: MongoDB に接続できない
**A**:
- MONGODB_URI が正しくコピーされたか確認
- MongoDB Atlas で IP ホワイトリストに Render の IP を追加：
  ```
  https://cloud.mongodb.com/v2/YOUR_ORG_ID#/org/security/whitelist
  ```
- または、すべての IP を許可（0.0.0.0/0）

### Q: JWT エラーが表示される
**A**:
- JWT_SECRET と JWT_REFRESH_SECRET が正確にコピーされたか確認
- 前後にスペースがないか確認
- Render を再デプロイ

---

## 🚀 クイックチェックリスト

環境変数設定の完全なチェックリスト：

- [ ] **Settings** ページにアクセスした
- [ ] **Environment** セクションが表示されている
- [ ] **REGISTRATION_ENABLED = true** を追加した
- [ ] **JWT_SECRET** を追加した
- [ ] **JWT_REFRESH_SECRET** を追加した
- [ ] **MONGODB_URI** を追加した
- [ ] **DB_NAME = librechat** を追加した
- [ ] **PORT = 3000** を追加した
- [ ] **METRICS_SECRET** を追加した
- [ ] **Save Changes** をクリックした
- [ ] **Deploy** をクリックした
- [ ] **5-10 分待機**した
- [ ] Logs で「Your service is live」を確認した
- [ ] https://librechat-9wa4.onrender.com にアクセス
- [ ] **Sign Up ボタン が表示されているか確認**

---

## 📞 サポート

何か不明な点があれば、以下をご確認ください：
- Render Logs: https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00/logs
- MongoDB Status: https://cloud.mongodb.com/

