#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LibreChat MongoDB 接続設定
"""

import os
from dotenv import load_dotenv

# .env ファイルを読み込み
load_dotenv()

# MongoDB 接続設定
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "librechat")

print("=" * 70)
print("LibreChat MongoDB Configuration")
print("=" * 70)
print()

if not MONGODB_URI:
    print("[ERROR] MONGODB_URI not set in .env file")
else:
    print("[OK] MongoDB Configuration:")
    print(f"    - Connection String: {MONGODB_URI[:50]}...")
    print(f"    - Database Name: {DB_NAME}")
    print()
    print("Environment Variables for LibreChat:")
    print(f"    - MONGODB_URI={MONGODB_URI}")
    print(f"    - DB_NAME={DB_NAME}")
    print()
    print("Add these to your .env file to enable:")
    print("    - Conversation History Storage")
    print("    - User Preferences")
    print("    - Chat Sessions")
    print()

print("=" * 70)
print("Note: Replace <db_password> with actual password")
print("=" * 70)