#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LibreChat ユーザー管理スクリプト
MongoDB に直接ユーザーを追加
"""

import os
import hashlib
import secrets
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# 環境変数を読み込み
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "librechat")

def hash_password(password):
    """パスワードをハッシュ化"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}${password_hash.hex()}"

def verify_password(stored_hash, password):
    """パスワードを検証"""
    salt, hash_hex = stored_hash.split('$')
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return hash_hex == password_hash.hex()

def connect_mongodb():
    """MongoDB に接続"""
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        # サーバー接続をテスト
        client.server_info()
        return client
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"[ERROR] MongoDB 接続失敗: {e}")
        return None

def create_user(username, email, password):
    """ユーザーを作成"""
    client = connect_mongodb()
    if not client:
        return False
    
    try:
        db = client[DB_NAME]
        users = db['users']
        
        # ユーザーが既に存在するか確認
        if users.find_one({"username": username}):
            print(f"[ERROR] ユーザー '{username}' は既に存在します")
            return False
        
        if users.find_one({"email": email}):
            print(f"[ERROR] メールアドレス '{email}' は既に登録されています")
            return False
        
        # 新しいユーザーを作成
        user_doc = {
            "username": username,
            "email": email,
            "password": hash_password(password),
            "provider": "local",
            "role": "user",
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
            "verified": True,
            "settings": {}
        }
        
        result = users.insert_one(user_doc)
        print(f"[OK] ユーザー '{username}' を作成しました")
        print(f"    - Email: {email}")
        print(f"    - User ID: {result.inserted_id}")
        return True
        
    except Exception as e:
        print(f"[ERROR] ユーザー作成失敗: {e}")
        return False
    finally:
        client.close()

def list_users():
    """ユーザー一覧を表示"""
    client = connect_mongodb()
    if not client:
        return
    
    try:
        db = client[DB_NAME]
        users = db['users']
        
        user_list = list(users.find({}, {"password": 0}))
        
        if not user_list:
            print("[INFO] ユーザーがまだ登録されていません")
            return
        
        print(f"[OK] 登録済みユーザー ({len(user_list)} 件):")
        print()
        for user in user_list:
            print(f"  - ユーザー名: {user.get('username')}")
            print(f"    Email: {user.get('email')}")
            print(f"    ロール: {user.get('role')}")
            print(f"     作成日: {user.get('createdAt')}")
            print()
            
    except Exception as e:
        print(f"[ERROR] ユーザー一覧取得失敗: {e}")
    finally:
        client.close()

def delete_user(username):
    """ユーザーを削除"""
    client = connect_mongodb()
    if not client:
        return False
    
    try:
        db = client[DB_NAME]
        users = db['users']
        
        result = users.delete_one({"username": username})
        
        if result.deleted_count == 0:
            print(f"[ERROR] ユーザー '{username}' が見つかりません")
            return False
        
        print(f"[OK] ユーザー '{username}' を削除しました")
        return True
        
    except Exception as e:
        print(f"[ERROR] ユーザー削除失敗: {e}")
        return False
    finally:
        client.close()

def main():
    """メイン処理"""
    print("=" * 70)
    print("LibreChat ユーザー管理ツール")
    print("=" * 70)
    print()
    
    if not MONGODB_URI:
        print("[ERROR] MONGODB_URI が .env に設定されていません")
        return
    
    while True:
        print("\n操作を選択:")
        print("  1. ユーザーを作成")
        print("  2. ユーザー一覧を表示")
        print("  3. ユーザーを削除")
        print("  4. 終了")
        print()
        
        choice = input("選択 (1-4): ").strip()
        
        if choice == "1":
            print()
            username = input("ユーザー名を入力: ").strip()
            email = input("メールアドレスを入力: ").strip()
            password = input("パスワードを入力: ").strip()
            
            if username and email and password:
                if create_user(username, email, password):
                    print()
                    print("[SUCCESS] ユーザーを作成しました！")
                    print(f"  ログイン URL: https://librechat-9wa4.onrender.com")
                    print(f"  ユーザー名: {username}")
                    print(f"  パスワード: {'*' * len(password)}")
            else:
                print("[ERROR] すべてのフィールドを入力してください")
        
        elif choice == "2":
            print()
            list_users()
        
        elif choice == "3":
            print()
            username = input("削除するユーザー名を入力: ").strip()
            if username:
                delete_user(username)
        
        elif choice == "4":
            print("\n終了します")
            break
        
        else:
            print("[ERROR] 無効な選択です")

if __name__ == "__main__":
    main()
