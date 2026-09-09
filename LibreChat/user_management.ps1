#!/usr/bin/env powershell
# LibreChat ユーザー作成スクリプト (PowerShell 版)

# 環境変数を読み込み
$envFile = Join-Path $PSScriptRoot ".env"
if (Test-Path $envFile) {
    $envContent = Get-Content $envFile -Raw
    $envContent -split "`n" | ForEach-Object {
        if ($_ -match "^([^=]+)=(.*)$") {
            $key = $matches[1]
            $value = $matches[2]
            [Environment]::SetEnvironmentVariable($key, $value, "Process")
        }
    }
}

$mongoUri = [Environment]::GetEnvironmentVariable("MONGODB_URI")
$dbName = [Environment]::GetEnvironmentVariable("DB_NAME", "librechat")

if (-not $mongoUri) {
    Write-Host "[ERROR] MONGODB_URI が .env に設定されていません" -ForegroundColor Red
    exit 1
}

Write-Host "=" * 70
Write-Host "LibreChat ユーザー管理ツール (PowerShell版)"
Write-Host "=" * 70
Write-Host ""

# MongoDB に接続するための情報表示
Write-Host "[INFO] MongoDB 接続情報:"
Write-Host "  URI: $($mongoUri.Substring(0, [Math]::Min(50, $mongoUri.Length)))..."
Write-Host "  Database: $dbName"
Write-Host ""

# ユーザー作成の案内
Write-Host "❌ Python がインストールされていないため、スクリプト実行ができません。"
Write-Host ""
Write-Host "✅ 代替案:"
Write-Host ""
Write-Host "方法 1: MongoDB Atlas Web UI で直接作成"
Write-Host "  1. https://cloud.mongodb.com にアクセス"
Write-Host "  2. Cluster0 → Collections → librechat → users"
Write-Host "  3. INSERT DOCUMENT をクリック"
Write-Host ""

Write-Host "方法 2: Render で REGISTRATION_ENABLED=true を設定"
Write-Host "  1. https://dashboard.render.com/web/srv-d8i4aa48aovs73f6ka00"
Write-Host "  2. Environment → REGISTRATION_ENABLED=true"
Write-Host "  3. Save をクリック"
Write-Host "  4. 5 分待機"
Write-Host "  5. https://librechat-9wa4.onrender.com で Sign Up"
Write-Host ""

Write-Host "方法 3: Node.js で直接実行（開発環境がある場合）"
Write-Host "  npm install"
Write-Host "  npm run build"
Write-Host ""

Write-Host "=" * 70
