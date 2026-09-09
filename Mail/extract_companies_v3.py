# -*- coding: utf-8 -*-
"""
FactLink Vietnam ホーチミン企業情報抽出スクリプト (v3)
検索結果ページから企業名・事業内容・URLを抽出（全ページ対象）
"""
import requests
from bs4 import BeautifulSoup
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
import time
import re
import os

class FactLinkSearchScraper:
    def __init__(self):
        self.base_url = "https://www.fact-link.com.vn"
        self.search_url_template = "https://www.fact-link.com.vn/search_result.php?id=003&type=prov&start={start}&lang=jp"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
        }
        self.session = requests.Session()
        self.companies = []
    
    def fetch_search_results(self, start=0):
        """検索結果ページから企業情報を直接抽出"""
        url = self.search_url_template.format(start=start)
        try:
            print(u"検索ページ取得中: start={}".format(start))
            
            if start == 0:
                self.session.cookies.set('PHPSESSID', 'auto', domain='www.fact-link.com.vn')
            
            response = self.session.get(url, headers=self.headers, timeout=60)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser')
            
            companies_data = []
            for span in soup.select('span.default_head'):
                a_tag = span.find('a')
                if a_tag and 'href' in a_tag.attrs:
                    name = a_tag.get_text(strip=True)
                    href = a_tag['href']
                    
                    if href.startswith('mem'):
                        full_url = self.base_url + '/' + href
                    elif href.startswith('http'):
                        full_url = href
                    else:
                        full_url = self.base_url + '/' + href
                    
                    td = a_tag.find_parent('td')
                    full_text = td.get_text(strip=True) if td else ''
                    business = full_text.replace(name, '', 1).strip()
                    
                    companies_data.append({
                        "name": name,
                        "business": business,
                        "address": "",
                        "email": "",
                        "website": full_url
                    })
                    
            print(u"  → {} 件取得".format(len(companies_data)))
            return companies_data
        except Exception as e:
            print(u"検索結果ページの取得に失敗: {}".format(str(e)))
            return []
    
    def scrape_all(self, max_pages=52, try_profiles=False):
        """全ページの企業情報を収集（start=0〜1530）"""
        print(u"ホーチミン企業リストの抽出を開始します...")
        print(u"(全 {} ページを対象)".format(max_pages))
        print()
        
        all_companies = []
        failed_pages = []
        
        for page in range(max_pages):
            start = page * 30
            companies = self.fetch_search_results(start=start)
            if companies:
                all_companies.extend(companies)
                print(u"  → 累計 {} 件".format(len(all_companies)))
            else:
                failed_pages.append(start)
                print(u"  [WARN] start={} 取得失敗（リトライします）".format(start))
                time.sleep(3)
                companies = self.fetch_search_results(start=start)
                if companies:
                    all_companies.extend(companies)
                    print(u"  → リトライ成功: 累計 {} 件".format(len(all_companies)))
                else:
                    print(u"  [SKIP] start={} スキップ".format(start))
            time.sleep(1.5)
        
        print(u"\n合計 {} 件の企業情報を取得しました".format(len(all_companies)))
        if failed_pages:
            print(u"失敗ページ: {}".format(failed_pages))
        
        if try_profiles and all_companies:
            print(u"\n=== プロフィールページからの詳細取得を試行 ===")
            for i, company in enumerate(all_companies):
                print(u"[{}/{}] {} ... ".format(i+1, len(all_companies), company['name'][:20]), end="")
                profile_data = self.try_fetch_profile(company['website'])
                company['address'] = profile_data['address']
                company['email'] = profile_data['email']
                time.sleep(1.5)
        
        self.companies = all_companies
        return self.companies
    
    def try_fetch_profile(self, profile_url):
        """プロフィールページから住所・メールを取得（試行）"""
        try:
            ref_headers = dict(self.headers)
            ref_headers['Referer'] = 'https://www.fact-link.com.vn/search_result.php?id=003&type=prov&start=0&lang=jp'
            
            response = self.session.get(profile_url, headers=ref_headers, timeout=30)
            response.encoding = 'utf-8'
            content = response.text.strip()
            
            if len(content) < 200 and 'meta' in content.lower() and 'refresh' in content.lower():
                print(u"  [SKIP] ブロックされました")
                return {"address": "", "email": ""}
            
            soup = BeautifulSoup(response.content, 'html.parser')
            page_text = soup.get_text("\n", strip=True)
            
            address = ""
            email = ""
            
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        label = cols[0].get_text(strip=True)
                        value = cols[1].get_text(strip=True)
                        
                        label_norm = re.sub(r"\s+", "", label)
                        if ('住所' in label_norm) or ('ADDRESS' in label.upper()) or ('Office' in label):
                            address = value
                        elif ('Email' in label) or ('メール' in label):
                            if '@' in value:
                                email = value
            
            if not email:
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                emails = re.findall(email_pattern, page_text)
                if emails:
                    email = emails[0]
            
            if not address:
                for line in page_text.splitlines():
                    if 'Ho Chi Minh' in line or 'ホーチミン' in line or 'TP.' in line:
                        address = line.strip()
                        break
            
            print(u"  [OK] 住所='{}' メール='{}'".format(
                address[:30] + "..." if len(address) > 30 else address,
                email if email else "なし"
            ))
            return {"address": address, "email": email}
            
        except Exception as e:
            print(u"  [ERR] プロフィール取得失敗: {}".format(str(e)))
            return {"address": "", "email": ""}
    
    def save_to_excel(self, output_path=None):
        """Excelファイルに保存"""
        if output_path is None:
            output_path = u"c:\\Users\\long\\OneDrive\\Code\\Mail\\ホーチミン企業リスト_全1403社.xlsx"
        
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
                print(u"既存ファイルを削除しました")
            except Exception as e:
                print(u"既存ファイルの削除に失敗: {}".format(str(e)))
        
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = u"ホーチミン企業リスト"
        
        headers = [u"No.", u"社名", u"事業内容", u"住所", u"メール", u"FactLinkウェブサイト"]
        ws.append(headers)
        
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF", size=11)
        
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
        for idx, company in enumerate(self.companies, 1):
            ws.append([
                idx,
                company["name"],
                company["business"],
                company["address"] if company["address"] else u"（要確認）",
                company["email"] if company["email"] else u"（要確認）",
                company["website"]
            ])
        
        ws.column_dimensions['A'].width = 5
        ws.column_dimensions['B'].width = 30
        ws.column_dimensions['C'].width = 45
        ws.column_dimensions['D'].width = 35
        ws.column_dimensions['E'].width = 28
        ws.column_dimensions['F'].width = 65
        
        for row in ws.iter_rows(min_row=2, max_row=len(self.companies)+1):
            for cell in row:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
                cell.font = Font(size=10)
        
        wb.save(output_path)
        print(u"\n[完了] ファイルが作成されました: {}".format(output_path))
        print(u"[完了] 合計 {} 社の情報を記録しました。".format(len(self.companies)))

    def print_summary(self):
        """結果サマリーを表示"""
        print(u"\n=== 抽出結果 ===")
        for idx, company in enumerate(self.companies, 1):
            print(u"\n{}. {}".format(idx, company['name']))
            print(u"   事業: {}".format(company['business'][:80]))
            addr = company['address'] if company['address'] else u"（未取得）"
            email = company['email'] if company['email'] else u"（未取得）"
            print(u"   住所: {}".format(addr))
            print(u"   メール: {}".format(email))
            print(u"   URL: {}".format(company['website']))


if __name__ == "__main__":
    import sys
    
    try_profiles = '--profiles' in sys.argv
    
    scraper = FactLinkSearchScraper()
    # start=0 〜 1530 (52ページ)
    companies = scraper.scrape_all(max_pages=52, try_profiles=try_profiles)
    
    scraper.save_to_excel()
    
    scraper.print_summary()