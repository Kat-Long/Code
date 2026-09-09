import asyncio
import csv
import os
from datetime import datetime
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv(r"C:\Scripts\.env")

# ===== 設定 =====
MA_SO_THUE = "0316200319"
USER_NAME  = "admin"
PASSWORD   = os.getenv("EINVOICE_PASSWORD")
OUTPUT_CSV = r"C:\Scripts\invoice_log.csv"
# ================

async def get_invoice_count():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # ログインページへ移動
        await page.goto("https://einvoice.com.vn/login", wait_until="load")

        # ログイン情報を入力
        await page.fill('input[name="maSoThue"]', MA_SO_THUE)
        await page.fill('input[name="userName"]',  USER_NAME)
        await page.fill('input[name="password"]',  PASSWORD)

        # お知らせポップアップを閉じる
        try:
            await page.wait_for_selector('#Dialog-ThongBaoLogin', timeout=3000)
            close_btn = page.locator('#Dialog-ThongBaoLogin [data-dismiss="modal"], #Dialog-ThongBaoLogin .close')
            if await close_btn.count() > 0:
                await close_btn.first.click()
            else:
                await page.keyboard.press('Escape')
            await page.wait_for_selector('#Dialog-ThongBaoLogin', state='hidden', timeout=5000)
        except:
            pass

        # ログインボタンをクリック＆ページ遷移を待つ
        async with page.expect_navigation(wait_until="load", timeout=30000):
            await page.click('#LuuLai')

       # 請求書一覧ページに直接移動
        await page.goto("https://einvoice.com.vn/danh-sach-hoa-don-dien-tu", wait_until="load")
        await asyncio.sleep(3)

        # 「昨日」を非表示のままJavaScriptで直接クリック
        await page.evaluate("document.querySelector('a.isYesterday').click()")

        # データ更新を待機
        await asyncio.sleep(2)
        await page.wait_for_function("""
            () => {
                const el = document.querySelector('#TatCaHD');
                return el && el.innerText.trim() !== '';
            }
        """, timeout=60000)

        count_text = await page.inner_text("#TatCaHD")

        await browser.close()
        return count_text.strip()

def save_to_csv(count):
    # 昨日の日付を記録
    from datetime import timedelta
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    recorded_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    file_exists = os.path.exists(OUTPUT_CSV)

    with open(OUTPUT_CSV, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["記録日時", "対象日付", "発行件数"])
        writer.writerow([recorded_at, yesterday, count])

    print(f"[{recorded_at}] 昨日({yesterday})の発行件数: {count} → 保存完了")

if __name__ == "__main__":
    if not PASSWORD:
        print("エラー: .env に EINVOICE_PASSWORD が設定されていません")
        exit(1)
    count = asyncio.run(get_invoice_count())
    save_to_csv(count)