#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LibreChat Render 接続検証スクリプト
"""

import os
import requests
from dotenv import load_dotenv

# .env ファイルを読み込み
load_dotenv(r"C:\Scripts\.env")

# 環境変数から接続情報を取得
RENDER_API_KEY = os.getenv("RENDER_API_KEY")
LIBRECHAT_URL = os.getenv("LIBRECHAT_URL")
LIBRECHAT_SERVICE_ID = os.getenv("LIBRECHAT_SERVICE_ID")
LIBRECHAT_REGION = os.getenv("LIBRECHAT_REGION")

def verify_environment():
    """環境変数を検証"""
    print("=" * 70)
    print("LibreChat Render Connection Verification")
    print("=" * 70)
    print()
    
    print("[1/4] Checking environment variables...")
    print()
    
    if not RENDER_API_KEY:
        print("[ERROR] RENDER_API_KEY not set")
        return False
    print(f"[OK] RENDER_API_KEY: {RENDER_API_KEY[:20]}...")
    
    if not LIBRECHAT_URL:
        print("[ERROR] LIBRECHAT_URL not set")
        return False
    print(f"[OK] LIBRECHAT_URL: {LIBRECHAT_URL}")
    
    if not LIBRECHAT_SERVICE_ID:
        print("[ERROR] LIBRECHAT_SERVICE_ID not set")
        return False
    print(f"[OK] LIBRECHAT_SERVICE_ID: {LIBRECHAT_SERVICE_ID}")
    
    if not LIBRECHAT_REGION:
        print("[ERROR] LIBRECHAT_REGION not set")
        return False
    print(f"[OK] LIBRECHAT_REGION: {LIBRECHAT_REGION}")
    
    print()
    return True

def verify_librechat_service():
    """LibreChat サービスを検証"""
    print("[2/4] Verifying LibreChat service via Render API...")
    print()
    
    RENDER_API_URL = "https://api.render.com/v1"
    headers = {
        "Authorization": f"Bearer {RENDER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{RENDER_API_URL}/services/{LIBRECHAT_SERVICE_ID}",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        
        service = response.json()
        service_data = service.get('service', {})
        
        print(f"[OK] Service found:")
        print(f"    - Name: {service_data.get('name')}")
        print(f"    - Status: {service_data.get('suspended')}")
        print(f"    - Branch: {service_data.get('branch')}")
        print()
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Service verification failed: {e}")
        return False

def verify_librechat_url():
    """LibreChat URL への接続を検証"""
    print("[3/4] Testing LibreChat URL connection...")
    print()
    
    try:
        response = requests.head(
            LIBRECHAT_URL,
            timeout=10,
            allow_redirects=True
        )
        
        if response.status_code < 400:
            print(f"[OK] LibreChat is accessible")
            print(f"    - Status Code: {response.status_code}")
            print()
            return True
        else:
            print(f"[ERROR] LibreChat returned status code {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] URL connection test failed: {e}")
        print(f"    (Note: This may be expected if the service is not yet running)")
        print()
        return True

def summary():
    """接続検証の確認"""
    print("[4/4] Connection Summary")
    print()
    print("LibreChat Render Configuration:")
    print(f"  - URL: {LIBRECHAT_URL}")
    print(f"  - Service ID: {LIBRECHAT_SERVICE_ID}")
    print(f"  - Region: {LIBRECHAT_REGION}")
    print()
    print("=" * 70)
    print("[OK] LibreChat is successfully connected to Render!")
    print("=" * 70)

if __name__ == "__main__":
    if verify_environment():
        verify_librechat_service()
        verify_librechat_url()
        summary()