# C:\Scripts\debug2.py として保存して実行
import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import os

load_dotenv(r"C:\Scripts\.env")

MA_SO_THUE = "0316200319"
USER_NAME  = "admin"
PASSWORD   = os.getenv("EINVOICE_PASSWORD")

async def debug():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # 画面表示
        page = await browser.new_page()

        await page.goto("https://einvoice.com.vn/login", wait_until="load")
        await page.fill('input[name="maSoThue"]', MA_SO_THUE)
        await page.fill('input[name="userName"]',  USER_NAME)
        await page.fill('input[name="password"]',  PASSWORD)

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

        async with page.expect_navigation(wait_until="load", timeout=30000):
            await page.click('#LuuLai')

        # 10秒待ってからページ状態を確認
        await asyncio.sleep(10)

        print("=== 現在のURL ===")
        print(page.url)

        # TatCaHD を含む要素を検索
        result = await page.evaluate("""() => {
            const el = document.querySelector('#TatCaHD');
            if (el) return 'FOUND: ' + el.outerHTML;

            // 'TatCa' を含むIDを全部探す
            const all = [...document.querySelectorAll('[id*="TatCa"]')];
            if (all.length) return 'SIMILAR: ' + all.map(e => e.id + '=' + e.innerText).join(', ');

            // 数字っぽい要素を探す
            const nums = [...document.querySelectorAll('[id*="HD"], [id*="hd"], [class*="count"], [class*="total"]')];
            return 'CANDIDATES: ' + nums.slice(0,10).map(e => e.id + '|' + e.className + '=' + e.innerText.trim()).join(' / ');
        }""")
        print("=== 要素検索結果 ===")
        print(result)

        input("ブラウザを確認してEnterで終了...")
        await browser.close()

asyncio.run(debug())