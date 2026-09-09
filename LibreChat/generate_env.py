#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Render デプロイ用の環境変数を生成
"""

import os
import uuid
import base64
from datetime import datetime

def generate_jwt_secret():
    """JWT シークレットを生成"""
    # UUID を使用して安全なシークレットを生成
    secret = str(uuid.uuid4()).replace('-', '') + str(uuid.uuid4()).replace('-', '')
    return secret[:64]

def generate_metrics_secret():
    """メトリクス用シークレットを生成"""
    return str(uuid.uuid4()).replace('-', '')

def main():
    print("=" * 70)
    print("LibreChat Render デプロイ - 環境変数生成ツール")
    print("=" * 70)
    print()
    
    # JWT シークレットを生成
    jwt_secret = generate_jwt_secret()
    jwt_refresh_secret = generate_jwt_secret()
    metrics_secret = generate_metrics_secret()
    
    print("生成された環境変数:")
    print()
    print(f"JWT_SECRET={jwt_secret}")
    print(f"JWT_REFRESH_SECRET={jwt_refresh_secret}")
    print(f"METRICS_SECRET={metrics_secret}")
    print()
    print("=" * 70)
    print()
    
    print("次のステップ:")
    print()
    print("1. Render ダッシュボードを開く:")
    print("   https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00")
    print()
    print("2. 'Environment' タブをクリック")
    print()
    print("3. 以下の環境変数を追加:")
    print()
    print("   [ Environment Variables ]")
    print(f"   JWT_SECRET = {jwt_secret}")
    print(f"   JWT_REFRESH_SECRET = {jwt_refresh_secret}")
    print(f"   METRICS_SECRET = {metrics_secret}")
    print(f"   PORT = 3000")
    print()
    print("4. 'Save' をクリック")
    print()
    print("5. 'Manual Deploy' をクリックしてデプロイを再実行")
    print()
    print("=" * 70)
    
    # .env ファイルに追加するかどうか
    response = input("\n.env ファイルに環境変数を保存しますか？ (y/n): ").strip().lower()
    
    if response == 'y':
        env_file = os.path.join(os.path.dirname(__file__), ".env")
        
        try:
            # 既存の .env ファイルを読み込み
            existing_vars = {}
            if os.path.exists(env_file):
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if '=' in line:
                                key, value = line.split('=', 1)
                                existing_vars[key] = value
            
            # 新しい変数を追加
            existing_vars['JWT_SECRET'] = jwt_secret
            existing_vars['JWT_REFRESH_SECRET'] = jwt_refresh_secret
            existing_vars['METRICS_SECRET'] = metrics_secret
            existing_vars['PORT'] = '3000'
            
            # .env ファイルに書き込み
            with open(env_file, 'w', encoding='utf-8') as f:
                for key, value in existing_vars.items():
                    f.write(f"{key}={value}\n")
            
            print(f"\n✓ .env ファイルに環境変数を保存しました: {env_file}")
            print("\n警告: .env ファイルをバージョン管理に含めないでください！")
            
        except Exception as e:
            print(f"\n✗ エラー: .env ファイルを保存できませんでした: {e}")
    
    print()
    print("完了！")

if __name__ == "__main__":
    main()
