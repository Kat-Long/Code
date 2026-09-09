# LibreChat Render デプロイ修正手順

## 現在のエラー

```
error: Failed to start server: JwtStrategy requires a secret or key
```

デプロイログから以下の問題が検出されました：

1. ✗ `librechat.yaml` ファイルが見つからない
2. ✗ JWT_SECRET が設定されていない
3. ✗ JWT_REFRESH_SECRET が設定されていない
4. ✗ ポート設定がない（デフォルトは 3000）

---

## 修正方法

### ステップ 1: Render ダッシュボードで環境変数を設定

**URL**: https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00

1. 画面左から **"Environment"** をクリック
2. 以下の環境変数を追加します

#### 必須環境変数

| Key | Value |
|-----|-------|
| `PORT` | `3000` |
| `JWT_SECRET` | `YOUR_GENERATED_JWT_SECRET` |
| `JWT_REFRESH_SECRET` | `YOUR_GENERATED_JWT_REFRESH_SECRET` |
| `ALLOW_SOCIAL_LOGIN` | `false` |
| `METRICTS_SECRET` | `your-metrics-secret-here` |

#### 既存の環境変数（確認）

| Key | Value |
|-----|-------|
| `MONGODB_URI` | `mongodb+srv://long1029_db_user:Cfgc5645@cluster0.c5czxzo.mongodb.net/?appName=Cluster0` |
| `DB_NAME` | `librechat` |

### ステップ 2: JWT シークレットを生成

Windows PowerShell で実行：
```powershell
$jwt1 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((Get-Random -Maximum 100000000000000000).ToString())) -replace '\+', '-' -replace '/', '_' -replace '=', ''
$jwt2 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((Get-Random -Maximum 100000000000000000).ToString())) -replace '\+', '-' -replace '/', '_' -replace '=', ''
Write-Host "JWT_SECRET=$jwt1"
Write-Host "JWT_REFRESH_SECRET=$jwt2"
```

または、ランダムな文字列を使用：
```
JWT_SECRET=aB1cD2eF3gH4iJ5kL6mN7oP8qR9sTuVwXyZ0AbCdEfGhIjKlMnOpQrStUvWxYzA
JWT_REFRESH_SECRET=xY9zAbCdEfGhIjKlMnOpQrStUvWxYzA1bC2dE3fG4hI5jK6lM7nO8pQ9rS0tU1v
```

### ステップ 3: `librechat.yaml` ファイルを作成

Render ダッシュボードでファイルをアップロードするか、以下のテンプレートを使用：

```yaml
version: 1.3.12

endpoints:
  openai:
    enabled: true
    type: openai
    apiKey: ${OPENAI_API_KEY}
    baseURL: https://api.openai.com/v1

  azure:
    enabled: false

  bingAI:
    enabled: false

plugins:
  enabled: true

registration:
  enabled: false

fileConfig:
  endpoints:
    - openai
    - assistants
  serverFileSizeLimit: 25
  avatarSizeLimit: 2

modelSpecs:
  - name: gpt-4
    label: GPT-4
    default: false
    costFactor: 30
  
  - name: gpt-3.5-turbo
    label: GPT-3.5 Turbo
    default: true
    costFactor: 1
```

### ステップ 4: Render でデプロイを再トリガー

1. Render ダッシュボードで **"Manual Deploy"** をクリック
2. または、以下のコマンドで再デプロイ：

```bash
python retry_deploy.py
```

---

## チェックリスト

- [ ] PORT=3000 を設定した
- [ ] JWT_SECRET を生成して設定した
- [ ] JWT_REFRESH_SECRET を生成して設定した
- [ ] MONGODB_URI が正しく設定されている
- [ ] DB_NAME=librechat が設定されている
- [ ] Render で環境変数の変更を保存した
- [ ] Manual Deploy で再デプロイを実行した

---

## トラブルシューティング

### デプロイがまだ失敗する場合

1. **ログを確認**
   ```bash
   python librechat_render.py
   ```

2. **MongoDB 接続を確認**
   ```bash
   python verify_librechat_connection.py
   ```

3. **サービス詳細を確認**
   ```bash
   python check_service_detail.py
   ```

### よくある問題

| 問題 | 解決方法 |
|-----|---------|
| `Port scan timeout` | PORT 環境変数を 3000 に設定 |
| `JWT Strategy error` | JWT_SECRET と JWT_REFRESH_SECRET を設定 |
| `Config file not found` | librechat.yaml をアップロード |
| `MongoDB connection error` | MONGODB_URI と DB_NAME を確認 |

---

## 参考リンク

- Render ダッシュボード: https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00
- LibreChat ドキュメント: https://www.librechat.ai/
- MongoDB ドキュメント: https://docs.mongodb.com/
