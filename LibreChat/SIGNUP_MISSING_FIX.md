# LibreChat 設定ファイル配置ガイド

## ⚠️ 問題の原因

「Sign Up」ボタンが表示されない理由は：

1. **librechat.yaml が Render にデプロイされていない**
   - ファイルが `/app/librechat.yaml` に配置されていない

2. **設定が認識されていない**
   - YAML フォーマットエラー
   - または設定キーが正しくない

3. **デプロイ後、設定の反映に遅延がある**

---

## ✅ 解決方法

### 方法 1: Render で環境変数を設定する（推奨）

環境変数で登録機能を有効化：

```
REGISTRATION_ENABLED=true
```

**Render ダッシュボード:**
1. https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00
2. "Environment" → "Add Environment Variable"
3. Key: `REGISTRATION_ENABLED`
4. Value: `true`
5. "Save"

### 方法 2: librechat.yaml をカスタムテキスト環境変数で設定

Render でカスタムファイルをマウント：

1. 環境変数で YAML を直接設定
2. または、アップロード用のディレクトリを指定

### 方法 3: Dockerfile で設定ファイルをコピー

Render が Git リポジトリから構築している場合：

1. `librechat.yaml` を Git リポジトリに追加
2. Git にコミット・プッシュ
3. Render で自動的に反映

---

## 🔍 LibreChat v0.8.6 での設定方法

LibreChat のバージョンによって設定方法が異なります。

**v0.8.6 での登録有効化:**

### 環境変数で設定

```
ALLOW_REGISTRATION=true
```

または

```
REGISTRATION_ENABLED=true
```

### librechat.yaml 設定

```yaml
version: 1.3.12

registration:
  enabled: true
```

---

## 📋 Render で環境変数を追加する手順

### ステップ 1: Render ダッシュボードを開く

```
https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00
```

### ステップ 2: 「Settings」タブをクリック

### ステップ 3: 「Environment」をクリック

### ステップ 4: 新しい環境変数を追加

| Key | Value |
|-----|-------|
| `REGISTRATION_ENABLED` | `true` |
| `ALLOW_REGISTRATION` | `true` |

### ステップ 5: 「Save」をクリック

---

## 🚀 変更後のデプロイ

環境変数を変更した後、自動的に再デプロイされます。

1. ダッシュボードで自動デプロイを確認
2. または「Manual Deploy」をクリック
3. ブラウザをリロード（5 分待機）

---

## 🔧 Git リポジトリから構築している場合

LibreChat をカスタマイズしている場合：

### ステップ 1: librechat.yaml を追加

プロジェクトのルートに `librechat.yaml` を配置：

```
your-repo/
├── librechat.yaml
├── package.json
└── ...
```

### ステップ 2: Git にコミット

```bash
git add librechat.yaml
git commit -m "Add LibreChat configuration with registration enabled"
git push origin main
```

### ステップ 3: Render が自動デプロイ

Git リポジトリが連携している場合、自動的に反映

---

## ✨ 別の設定オプション

### ソーシャルログインを有効化

```yaml
socialLogins:
  enabled: true
```

### プラグインを有効化

```yaml
plugins:
  enabled: true
```

### ロギングレベルを設定

```yaml
logging:
  level: debug  # info, debug, warn, error
```

---

## 🔍 トラブルシューティング

### 設定が反映されない

1. **キャッシュをクリア**
   ```
   Ctrl + Shift + Delete (Windows/Linux)
   Cmd + Shift + Delete (Mac)
   ```

2. **ブラウザをリロード**
   ```
   Ctrl + F5 (強制リロード)
   ```

3. **5-10 分待機**（デプロイ反映の遅延）

4. **Render ダッシュボードでデプロイ状態を確認**

### 設定が無視されている

1. YAML フォーマットエラーをチェック
2. インデント（スペース/タブ）を確認
3. キー名のタイポを確認

### 依然として Sign Up が表示されない

1. Render ログを確認
   - https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00 → Logs

2. ブラウザコンソールを確認
   - F12 → Console タブで JavaScript エラーを確認

3. LibreChat GitHub Issues を確認
   - https://github.com/danny-avila/LibreChat/issues

---

## 💡 クイックチェックリスト

- [ ] Render ダッシュボードで環境変数を設定した
- [ ] `REGISTRATION_ENABLED=true` を設定した
- [ ] 「Save」をクリックした
- [ ] 5-10 分待機した
- [ ] ブラウザをリロードした
- [ ] シークレットモード（プライベートブラウジング）で確認した
- [ ] 「Sign Up」ボタンが表示されているか確認した

---

**推奨: Render で環境変数 `REGISTRATION_ENABLED=true` を設定してください！** 🚀
