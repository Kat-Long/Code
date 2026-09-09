#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv

# .env を読み込み
load_dotenv()

RENDER_API_KEY = os.getenv("RENDER_API_KEY")
SERVICE_ID = os.getenv("LIBRECHAT_SERVICE_ID")
REGISTRATION_ENABLED = os.getenv("REGISTRATION_ENABLED")
ALLOW_REGISTRATION = os.getenv("ALLOW_REGISTRATION")

print("=" * 70)
print("Environment Variables Check")
print("=" * 70)
print()

print("[Local .env ファイル]")
print(f"RENDER_API_KEY: {RENDER_API_KEY[:20] if RENDER_API_KEY else 'NOT SET'}...")
print(f"LIBRECHAT_SERVICE_ID: {SERVICE_ID if SERVICE_ID else 'NOT SET'}")
print(f"REGISTRATION_ENABLED: {REGISTRATION_ENABLED if REGISTRATION_ENABLED else 'NOT SET'}")
print(f"ALLOW_REGISTRATION: {ALLOW_REGISTRATION if ALLOW_REGISTRATION else 'NOT SET'}")
print()

# Render API で確認
if RENDER_API_KEY and SERVICE_ID:
    print("[Render API での確認]")
    headers = {"Authorization": f"Bearer {RENDER_API_KEY}"}
    url = f"https://api.render.com/v1/services/{SERVICE_ID}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✓ Render API 接続成功")
            print()
            
            # 環境変数を取得（APIには通常環境変数は返されないため、サービス情報のみ）
            print(f"Service Name: {data.get('name', 'N/A')}")
            print(f"Status: {data.get('suspended', 'N/A')}")
            print(f"URL: {data.get('serviceDetails', {}).get('url', 'N/A')}")
        else:
            print(f"✗ API エラー: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ 接続エラー: {e}")
else:
    print("[Render API での確認]")
    print("✗ RENDER_API_KEY または SERVICE_ID が設定されていません")

print()
print("=" * 70)
print("Render ダッシュボードで確認してください:")
print("https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00")
print("Settings → Environment")
print("=" * 70)