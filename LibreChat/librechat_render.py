#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Render API を使用して Librechat インスタンスに接続
"""

import os
import requests
from dotenv import load_dotenv

# Load .env from the current directory
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# 環境変数から API キーを取得
RENDER_API_KEY = os.getenv("RENDER_API_KEY")

if not RENDER_API_KEY:
    print("エラー: RENDER_API_KEY が .env ファイルに設定されていません")
    exit(1)

# Render API の基本 URL
RENDER_API_URL = "https://api.render.com/v1"

# リクエストヘッダー
headers = {
    "Authorization": f"Bearer {RENDER_API_KEY}",
    "Content-Type": "application/json"
}

def get_librechat_service():
    """Render 上の Librechat サービスを取得"""
    try:
        # まずプロジェクト一覧を取得
        response = requests.get(
            f"{RENDER_API_URL}/projects",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        
        projects = response.json()
        
        # 各プロジェクト内のサービスを検索
        for project in projects:
            project_id = project.get('id')
            if not project_id:
                continue
            
            # プロジェクト内のサービスを取得
            try:
                services_response = requests.get(
                    f"{RENDER_API_URL}/projects/{project_id}/services",
                    headers=headers,
                    timeout=10
                )
                services_response.raise_for_status()
                services = services_response.json()
                
                # Librechat サービスを検索（大文字小文字を区別しない）
                for service in services:
                    service_name = service.get("name", "").lower()
                    if "librechat" in service_name or "my project" in service_name:
                        return service
                        
            except requests.exceptions.RequestException:
                continue
        
        # サービスが見つからない場合は、全サービスから検索
        try:
            response = requests.get(
                f"{RENDER_API_URL}/services",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            services = response.json()
            
            # Librechat サービスを検索
            for service in services:
                if "librechat" in service.get("name", "").lower():
                    return service
        except:
            pass
        
        print("Librechat サービスが見つかりませんでした")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"エラー: Render API への接続に失敗しました: {e}")
        return None

def get_service_details(service_id):
    """Render サービスの詳細情報を取得"""
    try:
        response = requests.get(
            f"{RENDER_API_URL}/services/{service_id}",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"エラー: サービス詳細の取得に失敗しました: {e}")
        return None

def test_render_connection():
    """Render API への接続テスト"""
    try:
        response = requests.get(
            f"{RENDER_API_URL}/services",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("[OK] Render API への接続に成功しました")
            return True
        elif response.status_code == 401:
            print("[ERROR] エラー: API キーが無効です")
            return False
        else:
            print(f"[ERROR] エラー: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] エラー: 接続に失敗しました: {e}")
        return False

def main():
    """メイン処理"""
    print("=" * 50)
    print("Render API - Librechat 接続テスト")
    print("=" * 50)
    print()
    
    # 接続テスト
    print("[1/3] Render API への接続をテスト中...")
    if not test_render_connection():
        return
    print()
    
    # Librechat サービスを検索
    print("[2/3] Librechat サービスを検索中...")
    service = get_librechat_service()
    if service:
        print(f"[OK] Librechat サービスが見つかりました:")
        print(f"  - サービス ID: {service.get('id')}")
        print(f"  - サービス名: {service.get('name')}")
        print(f"  - ステータス: {service.get('status')}")
        print(f"  - URL: {service.get('service_details', {}).get('url')}")
    else:
        print("[ERROR] Librechat サービスが見つかりません")
        return
    print()
    
    # サービス詳細を取得
    print("[3/3] サービス詳細を取得中...")
    service_id = service.get('id')
    if service_id:
        details = get_service_details(service_id)
        if details:
            print("[OK] サービス詳細:")
            print(f"  - 名前: {details.get('name')}")
            print(f"  - タイプ: {details.get('type')}")
            print(f"  - 環境: {details.get('env')}")
            print(f"  - 作成日: {details.get('createdAt')}")
    print()
    
    print("=" * 50)
    print("接続テスト完了")
    print("=" * 50)

if __name__ == "__main__":
    main()