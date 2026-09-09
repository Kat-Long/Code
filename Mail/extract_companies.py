# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
import time
import re
import os

class FactLinkScraper:
    def __init__(self):
        self.base_url = "https://www.fact-link.com.vn"
        self.search_url_template = "https://www.fact-link.com.vn/search_result.php?id=003&type=prov&start={start}&lang=jp"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.companies = []
    
    def fetch_search_results(self):
        """ホーチミン検索結果ページから企業リンクを取得"""
        try:
            response = requests.get(self.search_url, headers=self.headers, timeout=60)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 企業リンクを抽出
            company_links = []
            for link in soup.find_all('a', href=re.compile(r'mem_profile\.php')):
                href = link.get('href')
                if 'lang=jp' in href and href not in company_links:
                    full_url = self.base_url + '/' + href if href.startswith('mem') else href
                    company_links.append(full_url)
            
            print(u"検索結果から {} 件の企業リンクを取得しました".format(len(company_links)))
            return company_links
        except Exception as e:
            print(u"検索結果ページの取得に失敗しました: {}".format(str(e)))
            return []
    
    def extract_company_info(self, profile_url):
        """企業プロフィールページから情報を抽出"""
        try:
            print(u"[DEBUG] fetching profile={}".format(profile_url))
            # リトライ用
            last_err = None
            for attempt in range(3):
                try:
                    response = requests.get(profile_url, headers=self.headers, timeout=60)
                    response.encoding = 'utf-8'
                    break
                except Exception as e:
                    last_err = e
                    time.sleep(2)
            else:
                raise last_err

            print(u"[DEBUG] profile status={} encoding={}".format(getattr(response, 'status_code', None), getattr(response, 'encoding', None)))
            soup = BeautifulSoup(response.content, 'html.parser')
            
            company_info = {
                "name": "",
                "business": "",
                "address": "",
                "email": "",
                "website": profile_url
            }
            
            # 社名を抽出
            title_elem = soup.find('h1')
            if title_elem:
                company_info["name"] = title_elem.get_text(strip=True)
            else:
                title_tag = soup.find('title')
                if title_tag:
                    company_info["name"] = title_tag.get_text(strip=True)
            
            # テーブルから情報を抽出
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        label = cols[0].get_text(strip=True)
                        value = cols[1].get_text(strip=True)
                        
                        label_norm = re.sub(r"\s+", "", label)
                        # 事業内容/住所/メールはラベル表記ゆれがあるので部分一致
                        if ('事業内容' in label_norm) or ('事業' in label_norm):
                            company_info["business"] = value
                        elif ('住所' in label_norm) or ('ADDRESS' in label.upper()) or ('Office' in label):
                            company_info["address"] = value
                        elif ('Email' in label) or ('メール' in label) or ('@' in value):
                            if '@' in value:
                                company_info["email"] = value
            
            # テーブル内で取れなかった場合はテキストから住所/メールを再探索
            page_text = soup.get_text("\n", strip=True)

            if not company_info["address"]:
                # 住所らしき行を抽出（簡易）
                # 例: 'ホーチミンオフィス 602/43 ...'
                addr_candidates = []
                for line in page_text.splitlines():
                    if 'Ho Chi Minh' in line or 'ホーチミン' in line or 'TP.' in line:
                        addr_candidates.append(line.strip())
                if addr_candidates:
                    company_info["address"] = addr_candidates[0]

            if not company_info["email"]:
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                emails = re.findall(email_pattern, page_text)
                if emails:
                    company_info["email"] = emails[0]

            # デバッグ出力（最初の1社だけなどに絞りたい場合はここを調整）
            if (company_info.get("name")):
                preview = page_text[:120].replace("\n", " ")
                print(u"[DEBUG] name={}".format(company_info.get("name")))
                print(u"[DEBUG] URL={}".format(profile_url))
                print(u"[DEBUG] business='{}'".format(company_info.get("business", "")))
                print(u"[DEBUG] address='{}'".format(company_info.get("address", "")))
                print(u"[DEBUG] email='{}'".format(company_info.get("email", "")))
                print(u"[DEBUG] page_text_preview={}".format(preview))

            # 取得できていない場合の追加デバッグ（住所/メールが空）
            if (company_info.get("name") and (not company_info["address"] or not company_info["email"])):
                # tableラベルを収集して確認
                table_labels = []
                for table in tables:
                    for row in table.find_all('tr'):
                        cols = row.find_all('td')
                        if len(cols) >= 2:
                            lbl = cols[0].get_text(strip=True)
                            val = cols[1].get_text(strip=True)
                            table_labels.append((lbl, val))
                print(u"[DEBUG] table label/value count={}".format(len(table_labels)))
                for lbl, val in table_labels[:30]:
                    lbl_norm = re.sub(r"\s+", "", lbl)
                    print(u"[DEBUG]  label='{}' (norm='{}') value='{}'".format(lbl, lbl_norm, val))

            return company_info
            
        except Exception as e:
            print(u"プロフィールページの取得に失敗: {} (URL: {})".format(str(e), profile_url))
            return None
    
    def scrape_all(self):
        # 失敗URL用
        failed_urls_path = u"c:\\Users\\long\\OneDrive\\Code\\Mail\\factlink_failed_urls.txt"
        failed_urls = []
        """すべての企業情報をスクレイピング"""
        print(u"ホーチミン企業リストの抽出を開始します...")
        all_links = []

        # テスト運用：まずは2ページ（start=0,30）分のみ（候補=最大60件）
        for start in range(0, 61, 30):
            self.search_url = self.search_url_template.format(start=start)
            print(u"-- search start={} --".format(start))
            links = self.fetch_search_results()
            for l in links:
                if l not in all_links:
                    all_links.append(l)
            time.sleep(1)

        company_links = all_links
        print(u"合計候補リンク: {}".format(len(company_links)))

        # ここからプロフィール取得（テスト運用）
        for idx, link in enumerate(company_links, 1):
            if idx > 3:
                break
            print(u"[{}/{}] を処理中...".format(idx, len(company_links)))
            company_info = self.extract_company_info(link)
            
            if company_info:
                self.companies.append(company_info)
                print(u"  [OK] {}".format(company_info.get('name', '')))
            else:
                # 取得失敗/例外など
                print("  [NG] 抽出失敗")
                failed_urls.append(link)
            time.sleep(1)  # サーバーへの負荷軽減
        
        # 失敗URLを保存
        if failed_urls:
            with open(failed_urls_path, "w", encoding="utf-8") as f:
                for u in failed_urls:
                    f.write(u + "\n")
            print(u"失敗URLを保存しました: {}".format(failed_urls_path))
        else:
            print(u"失敗URLはありませんでした")

        return self.companies
    
    def save_to_excel(self, output_path=None):
        """Excelファイルに保存"""
        if output_path is None:
            output_path = u"c:\\Users\\long\\OneDrive\\Code\\Mail\\ホーチミン企業リスト.xlsx"
        
        # 既存ファイルは上書き保存（ロック時は失敗するため、メッセージを出す）
        if os.path.exists(output_path):
            print(u"既存ファイルは上書きします: {}".format(output_path))
        
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = u"ホーチミン企業リスト"
        
        # ヘッダー行の設定
        headers = [u"No.", u"社名", u"事業内容", u"住所", u"メール", u"FactLinkベトナムウェブサイト"]
        ws.append(headers)
        
        # ヘッダーのスタイル設定
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")
        
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
        # データ行の追加
        for idx, company in enumerate(self.companies, 1):
            ws.append([
                idx,
                company["name"],
                company["business"],
                company["address"],
                company["email"],
                company["website"]
            ])
        
        # 列幅の自動調整
        ws.column_dimensions['A'].width = 5
        ws.column_dimensions['B'].width = 25
        ws.column_dimensions['C'].width = 40
        ws.column_dimensions['D'].width = 35
        ws.column_dimensions['E'].width = 25
        ws.column_dimensions['F'].width = 60
        
        # セルの自動折り返し設定
        for row in ws.iter_rows(min_row=2, max_row=len(self.companies)+1):
            for cell in row:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
                cell.font = Font(size=10)
        
        wb.save(output_path)
        print(u"\n[完了] ファイルが作成されました")
        print(u"[完了] 合計 {} 社の情報を記録しました。".format(len(self.companies)))

# メイン処理
if __name__ == "__main__":
    scraper = FactLinkScraper()
    companies = scraper.scrape_all()
    scraper.save_to_excel()
    
    print(u"\n=== 抽出結果 ===")
    for idx, company in enumerate(companies, 1):
        print(u"\n{}. {}".format(idx, company['name']))
        print(u"   事業: {}".format(company['business']))
        print(u"   住所: {}".format(company['address']))
        print(u"   メール: {}".format(company['email']))
