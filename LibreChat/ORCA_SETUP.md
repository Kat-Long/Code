# 🚀 Orca モデル設定ガイド

## ✅ 完了した変更

`librechat.yaml` に Orca エンドポイントを追加しました：

```yaml
orca:
  enabled: true
  type: openai
  apiKey: ${ORCA_API_KEY}
  baseURL: https://api.orcarouter.ai/v1
  models:
    default: ["fable"]
```

---

## 📋 Render に設定すべき環境変数

### ステップ 1: Render ダッシュボードを開く

```
https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00
```

### ステップ 2: Settings → Environment をクリック

左メニューから **Settings** > **Environment** に移動

### ステップ 3: 以下の環境変数を追加・更新

| 変数名 | 値 |
|-------|-----|
| `OPENAI_API_KEY` | `sk-orca-w9aLZIybny6b2vs4sU9e75BN0OY3GBVbzxkkLeCMN92` |
| `ORCA_API_KEY` | `sk-orca-w9aLZIybny6b2vs4sU9e75BN0OY3GBVbzxkkLeCMN92` |

### ステップ 4: Save をクリック

変更を保存します

### ステップ 5: Manual Deploy を実行

```
Dashboard → Deploy → Redeploy latest commit
```

デプロイが完了するまで待機します（5〜10分）

---

## 🔍 デプロイ完了後の確認

### 方法 1: Render ダッシュボードで確認

1. **Logs** タブを開く
2. 以下のログが表示されることを確認：
   ```
   ==> Build successful
   ==> Starting service
   ==> Service started successfully
   ```

### 方法 2: LibreChat アプリで確認

1. https://librechat-9wa4.onrender.com にアクセス
2. ログイン
3. チャットで **Orca Fable** モデルが選択可能か確認

---

## 📝 設定内容

### OpenAI API キー
```
sk-orca-w9aLZIybny6b2vs4sU9e75BN0OY3GBVbzxkkLeCMN92
```

### Orca API エンドポイント
```
https://api.orcarouter.ai/v1/chat/completions
```

### 利用可能モデル
- `fable`

---

## ⚙️ ローカル動作確認（オプション）

ローカルで動作確認したい場合：

```bash
cd c:\Users\long\OneDrive\Code\LibreChat
echo "ORCA_API_KEY=sk-orca-w9aLZIybny6b2vs4sU9e75BN0OY3GBVbzxkkLeCMN92" >> .env
npm start
```

---

## ⚠️ セキュリティ注意

- `.env` ファイルを Git にコミットしないこと
- API キーを共有しないこと
- 本番環境では Render ダッシュボードで直接設定すること

---

## 🆘 トラブルシューティング

### Orca モデルが表示されない

1. Render のログで環境変数が設定されているか確認
2. `ORCA_API_KEY` が正しく設定されているか確認
3. Manual Deploy で再デプロイ

### API エラーが出る場合

- API キーが正しいか確認
- ネットワーク接続を確認
- Render ダッシュボードのログで詳細エラーを確認

---

完了後、デプロイスクリプトを実行してください：

```bash
python retry_deploy.py
```
