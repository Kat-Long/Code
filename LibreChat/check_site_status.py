#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LibreChat サイト状態確認ツール
"""

import os
import requests
import json
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

LIBRECHAT_URL = os.getenv("LIBRECHAT_URL", "https://librechat-9wa4.onrender.com")

def check_server_status():
    """サーバーステータスを確認"""
    print("=" * 70)
    print("LibreChat サイト状態確認")
    print("=" * 70)
    print()
    
    try:
        print("[1/5] サーバーの応答を確認中...")
        response = requests.get(LIBRECHAT_URL, timeout=10, verify=False)
        
        if response.status_code == 200:
            print(f"[OK] サーバーが応答しています (Status: {response.status_code})")
        else:
            print(f"[WARN] 予期しないステータス: {response.status_code}")
        
        print()
        
        # API エンドポイントを確認
        print("[2/5] API エンドポイントの確認...")
        
        api_endpoints = [
            "/api/auth/login",
            "/api/auth/register",
            "/api/config",
            "/api/user"
        ]
        
        for endpoint in api_endpoints:
            try:
                api_response = requests.get(
                    f"{LIBRECHAT_URL}{endpoint}",
                    timeout=5,
                    verify=False
                )
                status = "✓" if api_response.status_code < 500 else "✗"
                print(f"  {status} {endpoint}: {api_response.status_code}")
            except Exception as e:
                print(f"  ✗ {endpoint}: エラー ({str(e)[:30]}...)")
        
        print()
        
        # 設定を確認
        print("[3/5] LibreChat 設定の確認...")
        try:
            config_response = requests.get(
                f"{LIBRECHAT_URL}/api/config",
                timeout=5,
                verify=False
            )
            
            if config_response.status_code == 200:
                config = config_response.json()
                
                # 重要な設定項目をチェック
                registration = config.get('registration', {})
                print(f"  Registration enabled: {registration.get('enabled', 'Unknown')}")
                
                models = config.get('models', [])
                print(f"  Available models: {len(models)}")
                
                print("[OK] 設定情報を取得しました")
            else:
                print(f"[WARN] 設定エンドポイント: {config_response.status_code}")
        except Exception as e:
            print(f"[WARN] 設定情報取得失敗: {e}")
        
        print()
        
        # ログイン画面を確認
        print("[4/5] ログイン画面の確認...")
        try:
            login_response = requests.get(
                f"{LIBRECHAT_URL}/auth/login",
                timeout=5,
                verify=False
            )
            
            if "login" in login_response.text.lower() or "sign" in login_response.text.lower():
                print("[OK] ログイン画面が利用可能")
                
                # Sign Up の存在を確認
                if "sign up" in login_response.text.lower() or "signup" in login_response.text.lower() or "register" in login_response.text.lower():
                    print("[OK] Sign Up/Register ボタンが見つかりました！")
                else:
                    print("[WARN] Sign Up ボタンが見つかりません")
            else:
                print("[WARN] ログイン画面が見つかりません")
        except Exception as e:
            print(f"[WARN] ログイン画面確認失敗: {e}")
        
        print()
        
        # MongoDB 接続状態を推測
        print("[5/5] バックエンド接続の推測...")
        try:
            health_response = requests.get(
                f"{LIBRECHAT_URL}/api/health",
                timeout=5,
                verify=False
            )
            
            if health_response.status_code == 200:
                print("[OK] ヘルスチェック成功 - バックエンド正常")
            else:
                print(f"[WARN] ヘルスチェック: {health_response.status_code}")
        except Exception as e:
            print(f"[WARN] ヘルスチェック失敗")
        
        print()
        print("=" * 70)
        print("\n📋 推奨される次のステップ:\n")
        print("1. Render ダッシュボードで環境変数を確認")
        print("   https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00\n")
        print("2. 以下の環境変数が設定されているか確認:")
        print("   - REGISTRATION_ENABLED=true")
        print("   - ALLOW_REGISTRATION=true\n")
        print("3. ブラウザをリロード (Ctrl+F5)")
        print("4. https://librechat-9wa4.onrender.com/auth/login にアクセス\n")
        print("=" * 70)
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] サーバーに接続できません: {e}")
        print()
        print("原因の可能性:")
        print("  - サーバーが起動していない")
        print("  - ネットワーク接続がない")
        print("  - Render でデプロイが失敗している")
        print()
        print("解決方法:")
        print("  1. Render ダッシュボードを確認")
        print("  2. 最新のログを確認")
        print("  3. 環境変数が正しく設定されているか確認")

if __name__ == "__main__":
    check_server_status()
