#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LibreChat デプロイ再試行スクリプト
"""

import os
import requests
from dotenv import load_dotenv

# Load .env from the current directory
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

RENDER_API_KEY = os.getenv("RENDER_API_KEY")
LIBRECHAT_SERVICE_ID = os.getenv("LIBRECHAT_SERVICE_ID")

RENDER_API_URL = "https://api.render.com/v1"

headers = {
    "Authorization": f"Bearer {RENDER_API_KEY}",
    "Content-Type": "application/json"
}

def retry_deploy():
    """デプロイを再試行"""
    print("=" * 70)
    print("LibreChat Deploy Retry")
    print("=" * 70)
    print()
    
    try:
        response = requests.post(
            f"{RENDER_API_URL}/services/{LIBRECHAT_SERVICE_ID}/deploys",
            headers=headers,
            json={},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print()
        print("Response:")
        print(response.text)
        print()
        
        if response.status_code in [200, 201]:
            print("[OK] Deploy retry initiated successfully!")
            print("Please check the Render dashboard for progress:")
            print("https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00")
        else:
            print("[ERROR] Deploy retry failed!")
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")

if __name__ == "__main__":
    retry_deploy()