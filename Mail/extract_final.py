# -*- coding: utf-8 -*-
"""
最終版: ホーチミン企業リスト全ページ抽出 + Excel保存
メール・住所取得をプロフィールページから実装
（※プロフィール取得はブロックされやすいため、初期Cookie/Refererをv3寄せで調整）
"""
import requests
from bs4 import BeautifulSoup
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
import time
import os
import re


class Scraper:
    def __init__(self):
        self.base_url = "https://www.fact-link.com.vn"
        self.tpl = "https://www.fact-link.com.vn/search_result.php?id=003&type=prov&start={start}&lang=jp"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
        }
        self.session = requests.Session()
        self.companies = []

        # v3寄せの固定Referer（start=0検索ページ）
        self.search_referer = "https://www.fact-link.com.vn/search_result.php?id=003&type=prov&start=0&lang=jp"

    def fetch_search_results(self, start):
        url = self.tpl.format(start=start)
        try:
            # v3同等: start=0 の検索取得時点でPHPSESSIDをセットしておく
            if start == 0:
                try:
                    self.session.cookies.set("PHPSESSID", "auto", domain="www.fact-link.com.vn")
                except Exception:
                    pass
            r = self.session.get(url, headers=self.headers, timeout=20)
            r.encoding = "utf-8"
            soup = BeautifulSoup(r.content, "html.parser")

            items = []
            for span in soup.select("span.default_head"):
                a = span.find("a")
                if not (a and a.get("href")):
                    continue

                name = a.get_text(strip=True)
                href = a["href"]

                if href.startswith("mem"):
                    full_url = self.base_url + "/" + href
                else:
                    full_url = href

                td = a.find_parent("td")
                full_text = td.get_text(strip=True) if td else ""
                business = full_text.replace(name, "", 1).strip() if full_text else ""

                items.append(
                    {
                        "name": name,
                        "business": business,
                        "address": "",
                        "email": "",
                        "website": full_url,
                    }
                )

            return items
        except Exception:
            return None

    def try_fetch_profile(self, profile_url):
        """プロフィールページから住所・メールを取得"""
        try:
            ref_headers = dict(self.headers)
            # v3寄せ：検索ページからの参照ヘッダ
            ref_headers["Referer"] = self.search_referer

            response = self.session.get(profile_url, headers=ref_headers, timeout=30)
            response.encoding = "utf-8"
            content = response.text.strip()

            # ブロックっぽいケース（len(content) が極端に小さい/メタリフレッシュ）
            if len(content) < 200 and ("meta" in content.lower()) and ("refresh" in content.lower()):
                return {"address": "", "email": ""}

            soup = BeautifulSoup(response.content, "html.parser")
            page_text = soup.get_text("\n", strip=True)

            address = ""
            email = ""

            # 住所/メールが表(table)に入っている前提
            tables = soup.find_all("table")
            for table in tables:
                rows = table.find_all("tr")
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) < 2:
                        continue

                    label = cols[0].get_text(strip=True)
                    value = cols[1].get_text(strip=True)

                    label_norm = re.sub(r"\s+", "", label)

                    # 住所判定
                    if ("住所" in label_norm) or ("ADDRESS" in label.upper()) or ("Office" in label):
                        if value:
                            address = value

                    # メール判定
                    elif ("Email" in label) or ("メール" in label):
                        if "@" in value:
                            email = value

            # tableで見つからない場合、本文から正規表現でメール抽出
            if not email:
                email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
                emails = re.findall(email_pattern, page_text)
                if emails:
                    email = emails[0]

            # 住所が table から取れない場合の簡易推定
            if not address:
                for line in page_text.splitlines():
                    if ("Ho Chi Minh" in line) or ("ホーチミン" in line) or ("TP." in line):
                        address = line.strip()
                        break

            return {"address": address, "email": email}
        except Exception:
            return {"address": "", "email": ""}

    def run(self):
        print("Extracting all pages (start=0 to 1530)...")
        all_data = []
        empty_streak = 0

        for page in range(52):
            start = page * 30
            print(f"  start={start:4d}... ", end="", flush=True)

            # v3寄せ：start=0でPHPSESSIDを用意（プロフィールブロック回避目的）
            if start == 0:
                try:
                    self.session.cookies.set("PHPSESSID", "auto", domain="www.fact-link.com.vn")
                except Exception:
                    pass

                # 念のため start=0 検索ページにReferer付きで1回当てる
                try:
                    self.session.get(self.search_referer, headers=self.headers, timeout=20)
                except Exception:
                    pass

            data = self.fetch_search_results(start)
            if data is None:
                print("FAIL")
                empty_streak += 1
            elif len(data) == 0:
                print("0件")
                empty_streak += 1
            else:
                empty_streak = 0
                all_data.extend(data)
                print(f"{len(data):2d}件 (total={len(all_data):4d})")

            if empty_streak >= 5:
                print("  -> 5 consecutive empty/fail, stopping")
                break

            time.sleep(1.2)

        print(f"\nTotal: {len(all_data)} companies")
        self.companies = all_data
        return all_data

    def enrich_profiles(self, limit=None):
        """プロフィールページから住所・メールを埋める"""
        total = len(self.companies)
        if limit is not None:
            total = min(total, limit)

        print(f"\nFetching profiles for address/email (count={total})...")
        for i in range(total):
            c = self.companies[i]
            url = c["website"]
            print(f"[{i+1}/{total}] {c['name'][:20]} ... ", end="", flush=True)

            prof = self.try_fetch_profile(url)
            c["address"] = prof.get("address", "") or ""
            c["email"] = prof.get("email", "") or ""

            addr_short = (c["address"][:15] + "...") if len(c["address"]) > 15 else c["address"]
            email_short = c["email"] if c["email"] else "なし"
            print(f"住所='{addr_short}' メール='{email_short}'")
            time.sleep(1.5)

    def save(self):
        path = "ホーチミン企業リスト_全1403社.xlsx"
        if os.path.exists(path):
            os.remove(path)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "企業リスト"

        headers = ["No.", "社名", "事業内容", "住所", "メール", "FactLinkウェブサイト"]
        ws.append(headers)

        hf = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        hf2 = Font(bold=True, color="FFFFFF", size=11)
        for cell in ws[1]:
            cell.fill = hf
            cell.font = hf2
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        for i, c in enumerate(self.companies, 1):
            ws.append([i, c["name"], c["business"], c["address"], c["email"], c["website"]])

        ws.column_dimensions["A"].width = 5
        ws.column_dimensions["B"].width = 30
        ws.column_dimensions["C"].width = 45
        ws.column_dimensions["F"].width = 65

        for row in ws.iter_rows(min_row=2, max_row=len(self.companies) + 1):
            for cell in row:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
                cell.font = Font(size=10)

        wb.save(path)
        print(f"\nSaved: {path}")
        print(f"Total: {len(self.companies)} companies")

        email_count = sum(1 for c in self.companies if c.get("email"))
        addr_count = sum(1 for c in self.companies if c.get("address"))

        print(f"Address found: {addr_count}/{len(self.companies)}")
        print(f"Email found: {email_count}/{len(self.companies)}")


if __name__ == "__main__":
    s = Scraper()
    s.run()
    s.enrich_profiles(limit=None)
    s.save()