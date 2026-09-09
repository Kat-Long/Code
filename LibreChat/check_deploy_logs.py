#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LibreChat Render デプロイログを確認
"""

import os
import requests
from dotenv import load_dotenv

# Load .env from the current directory
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

RENDER_API_KEY = os.getenv("RENDER_API_KEY")
LIBRECHAT_SERVICE_ID = os.getenv("LIBRECHAT_SERVICE_ID")

if not RENDER_API_KEY or not LIBRECHAT_SERVICE_ID:
    print("[ERROR] RENDER_API_KEY or LIBRECHAT_SERVICE_ID not set")
    exit(1)

RENDER_API_URL = "https://api.render.com/v1"

headers = {
    "Authorization": f"Bearer {RENDER_API_KEY}",
    "Content-Type": "application/json"
}

def get_service_logs():
    """Render サービスのログを取得"""
    print("=" * 70)
    print("LibreChat Render デプロイログ")
    print("=" * 70)
    print()
    
    try:
        # サービス詳細を取得
        response = requests.get(
            f"{RENDER_API_URL}/services/{LIBRECHAT_SERVICE_ID}",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        
        service = response.json()
        
        print("[Service Info]")
        print(f"Name: {service.get('name')}")
        print(f"Status: {service.get('status')}")
        print(f"URL: {service.get('serviceDetails', {}).get('url')}")
        print()
        
        # 最後のデプロイ情報
        print("[Last Deploy]")
        print(f"Created At: {service.get('createdAt')}")
        print(f"Updated At: {service.get('updatedAt')}")
        print()
        
        # デプロイ一覧を取得
        deploys_response = requests.get(
            f"{RENDER_API_URL}/services/{LIBRECHAT_SERVICE_ID}/deploys",
            headers=headers,
            timeout=10
        )
        deploys_response.raise_for_status()
        
        deploys = deploys_response.json()
        
        if deploys:
            latest_deploy = deploys[0]
            print("[Latest Deploy Details]")
            print(f"Deploy ID: {latest_deploy.get('id')}")
            print(f"Status: {latest_deploy.get('status')}")
            print(f"Created: {latest_deploy.get('createdAt')}")
            print(f"Updated: {latest_deploy.get('updatedAt')}")
            print()
            
            if latest_deploy.get('status') == 'FAILED':
                print("[ERROR] Latest deploy failed!")
                print(f"Error: {latest_deploy.get('statusMessage')}")
            elif latest_deploy.get('status') == 'LIVE':
                print("[OK] Service is live!")
        
        print()
        print("=" * 70)
        print("Note: For detailed logs, visit Render dashboard:")
        print("https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00")
        print("=" * 70)
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to get logs: {e}")

if __name__ == "__main__":
    get_service_logs()
