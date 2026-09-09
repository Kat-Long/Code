# 🔴 Sign Up ボタンを有効にする手順

## 現在の状態
- ✅ 再デプロイが開始されました
- ❌ REGISTRATION_ENABLED がまだ設定されていない

## すぐに実施してください

### ステップ 1: Render ダッシュボードを開く
```
https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00
```

### ステップ 2: Environment を開く
1. 左側メニューの **Settings**
2. **Environment** タブをクリック

### ステップ 3: 環境変数を追加
1. **+ Add Environment Variable** をクリック
2. キー: `REGISTRATION_ENABLED`
3. 値: `true`
4. **Save Changes** をクリック

### ステップ 4: 再デプロイ完了を待つ
- Logs タブで「Your service is live 🎉」を確認
- 通常 5-10 分

### ステップ 5: ブラウザをリロード
```
Ctrl + F5
```

### ステップ 6: Sign Up ボタンを確認
```
https://librechat-9wa4.onrender.com
```

---

## ✅ 確認チェックリスト

- [ ] ダッシュボードで Settings → Environment を開いた
- [ ] REGISTRATION_ENABLED = true を設定した
- [ ] Save Changes をクリックした
- [ ] Logs で「Your service is live」を確認した
- [ ] Ctrl + F5 でブラウザをリロード
- [ ] Sign Up ボタンが表示されているか確認

---

**🚀 すぐに Render ダッシュボードで環境変数を設定してください！**
