# 🔧 「Sign Up」ボタンが表示されない - 解決ガイド

## 問題

LibreChat のログイン画面に「Sign Up」ボタンが表示されていない

## 原因

以下のいずれかが該当：

1. ✗ `registration` 設定が Render に反映されていない
2. ✗ `librechat.yaml` が `/app/` に配置されていない
3. ✗ 設定ファイルのフォーマットエラー
4. ✗ デプロイ後のキャッシュ問題

---

## ✅ クイック解決策（推奨順）

### 方法 1: 環境変数で有効化（最も確実）

**Render ダッシュボード:**
https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00

1. 「Settings」→「Environment」
2. 新しい環境変数を追加：

| Key | Value |
|-----|-------|
| `REGISTRATION_ENABLED` | `true` |

3. 「Save」をクリック
4. 自動で再デプロイ開始
5. 3-5 分待機
6. ブラウザをリロード (Ctrl+F5)

### 方法 2: ブラウザキャッシュをクリア

古いキャッシュが表示されている可能性：

**Chrome/Edge:**
- Ctrl + Shift + Delete
- 「全期間」を選択
- 「クッキーと他のサイトデータ」にチェック
- 「削除」をクリック

**Firefox:**
- Ctrl + Shift + Delete
- 「すべて」を選択
- 「削除」をクリック

その後、https://librechat-9wa4.onrender.com にアクセス

### 方法 3: シークレット/プライベートモードで確認

ブラウザのシークレットモード（プライベートブラウジング）で確認：

- Chrome: Ctrl + Shift + N
- Firefox: Ctrl + Shift + P
- Edge: Ctrl + Shift + InPrivate
- Safari: Cmd + Shift + N

https://librechat-9wa4.onrender.com にアクセス

---

## 🔍 現在の設定を確認

### librechat.yaml の確認

```bash
cd "c:\Users\long\OneDrive\Code\LibreChat"
cat librechat.yaml | findstr -i registration
```

期待される出力：
```yaml
registration:
  enabled: true
```

### .env ファイルの確認

```bash
cat .env | findstr -i registration
```

---

## 📋 LibreChat v0.8.6 での設定方法

### 完全な librechat.yaml 設定

```yaml
version: 1.3.12

registration:
  enabled: true          # ✅ ユーザー登録を有効化
  requireEmail: false    # メール確認なしで即座に登録可能
  allowMultipleAccounts: true

endpoints:
  openai:
    enabled: true

plugins:
  enabled: true

socialLogins:
  enabled: false
```

---

## 🚀 推奨される設定プロセス

### ステップ 1: 環境変数を設定

Render ダッシュボード → Environment:

```
REGISTRATION_ENABLED=true
ALLOW_REGISTRATION=true
```

### ステップ 2: 待機

デプロイの完了を待つ (3-5 分)

### ステップ 3: キャッシュをクリア

- ブラウザキャッシュをクリア
- または シークレットモードで確認

### ステップ 4: ページをリロード

Ctrl + F5 (強制リロード)

### ステップ 5: 確認

「Sign Up」ボタンが表示されているか確認

---

## 💻 サイト状態を確認するコマンド

```bash
cd "c:\Users\long\OneDrive\Code\LibreChat"
python check_site_status.py
```

このスクリプトで：
- サーバーの応答状態
- API エンドポイントの確認
- 設定情報の取得
- ログイン画面の確認

---

## 🔗 アクセス URL

### ログイン画面
```
https://librechat-9wa4.onrender.com
```

### 直接ログイン画面を開く
```
https://librechat-9wa4.onrender.com/auth/login
```

### 設定・環境変数の確認
```
https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00
```

---

## 📝 よくある質問

### Q: 設定を変更したのに反映されない

**A:** キャッシュをクリア
```
Ctrl + Shift + Delete (Windows)
Cmd + Shift + Delete (Mac)
```

### Q: どのくらい待つ必要がある？

**A:** 通常 3-5 分。最大 10 分まで待機してください。

### Q: 環境変数をどこに設定する？

**A:** Render ダッシュボード
- https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00
- Settings → Environment

### Q: Sign Up を表示させない方法は？

**A:** 環境変数を削除するか、`enabled: false` に設定

---

## 📊 設定チェックリスト

- [ ] Render で `REGISTRATION_ENABLED=true` を設定した
- [ ] 「Save」をクリックした
- [ ] 5 分待機した
- [ ] ブラウザキャッシュをクリアした
- [ ] Ctrl + F5 でリロードした
- [ ] シークレットモードで確認した
- [ ] 「Sign Up」ボタンが表示されているか確認した

---

## 🆘 それでも表示されない場合

### ステップ 1: Render ログを確認

https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00 → Logs

エラーメッセージを確認

### ステップ 2: ブラウザコンソールを確認

F12 → Console タブで JavaScript エラーを確認

### ステップ 3: GitHub Issues を確認

https://github.com/danny-avila/LibreChat/issues

同じ問題が報告されているか確認

### ステップ 4: MongoDB 接続を確認

```bash
python verify_librechat_connection.py
```

---

**🎯 推奨: まずは環境変数 `REGISTRATION_ENABLED=true` を Render で設定してください！** 🚀
