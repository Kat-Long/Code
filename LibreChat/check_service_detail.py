#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LibreChat サービス詳細を確認
"""

import os
import requests
from dotenv import load_dotenv
import json

# .env ファイルを読み込み
load_dotenv(r"C:\Scripts\.env")

# 環境変数から接続情報を取得
RENDER_API_KEY = os.getenv("RENDER_API_KEY")
LIBRECHAT_SERVICE_ID = os.getenv("LIBRECHAT_SERVICE_ID")

RENDER_API_URL = "https://api.render.com/v1"

headers = {
    "Authorization": f"Bearer {RENDER_API_KEY}",
    "Content-Type": "application/json"
}

def get_service_detail():
    """サービス詳細を取得"""
    try:
        response = requests.get(
            f"{RENDER_API_URL}/services/{LIBRECHAT_SERVICE_ID}",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        
        print("=" * 70)
        print("Service Detail Response")
        print("=" * 70)
        print()
        print(f"Status Code: {response.status_code}")
        print()
        print("Raw Response:")
        print(response.text)
        print()
        print("Formatted JSON:")
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")

def get_deploys():
    """デプロイを取得"""
    try:
        response = requests.get(
            f"{RENDER_API_URL}/services/{LIBRECHAT_SERVICE_ID}/deploys",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        
        print()
        print("=" * 70)
        print("Deploys Response")
        print("=" * 70)
        print()
        print(f"Status Code: {response.status_code}")
        print()
        print("Raw Response:")
        print(response.text)
        print()
        print("Formatted JSON:")
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")

if __name__ == "__main__":
    get_service_detail()
    get_deploys()