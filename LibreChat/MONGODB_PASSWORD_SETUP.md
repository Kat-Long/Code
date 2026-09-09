# MongoDB パスワード設定ガイド

## Google アカウント連携時のパスワード設定

MongoDB アカウントが Google アカウントにリンクされている場合でも、データベースユーザーのパスワードは別に設定する必要があります。

## 手順

### 1. MongoDB Atlas ダッシュボードにアクセス
- https://cloud.mongodb.com にアクセス
- Google アカウントでサインイン

### 2. データベースユーザーのパスワードを確認/設定

#### パスワード確認方法（既存ユーザー）:
1. Cluster0 > Security > Database Access
2. ユーザー「long1029_db_user」を確認
3. パスワードが表示されない場合は、ユーザーを削除して再作成

#### パスワード再設定方法:
1. Cluster0 > Security > Database Access
2. 「long1029_db_user」の「Edit」をクリック
3. 「Edit Password」で新しいパスワードを設定
4. パスワードをコピー

### 3. 接続文字列を更新

取得したパスワードを使用して、接続文字列を更新:

```
MONGODB_URI=mongodb+srv://long1029_db_user:YOUR_PASSWORD_HERE@cluster0.c5czxzo.mongodb.net/?appName=Cluster0
```

例:
```
MONGODB_URI=mongodb+srv://long1029_db_user:MySecurePassword123@cluster0.c5czxzo.mongodb.net/?appName=Cluster0
```

### 4. .env ファイルを更新

```bash
# .env ファイルを編集
nano .env

# または

code .env
```

以下の行を更新:
```
MONGODB_URI=mongodb+srv://long1029_db_user:YOUR_PASSWORD@cluster0.c5czxzo.mongodb.net/?appName=Cluster0
```

### 5. 接続テスト

```bash
python mongodb_config.py
```

## セキュリティ上の注意

- パスワードに特殊文字が含まれる場合は、URL エンコードが必要な場合があります
- .env ファイルは Git にコミットしないでください
- パスワードは定期的に変更してください
- 本番環境では環境変数として設定してください

## IP ホワイトリスト確認

MongoDB Atlas での接続を許可するために:

1. Cluster0 > Security > Network Access
2. IP ホワイトリストを確認
3. 必要に応じて「Allow access from anywhere (0.0.0.0/0)」を設定

## トラブルシューティング

### 接続エラーが表示される場合

1. **Authentication failed**
   - パスワードが正しいか確認
   - URL エンコードが必要か確認

2. **Connection timeout**
   - IP ホワイトリストを確認
   - MongoDB Atlas のステータスを確認

3. **Unknown database**
   - データベースが作成されるまで待機
   - DB_NAME が正しいか確認