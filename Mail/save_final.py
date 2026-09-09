# -*- coding: utf-8 -*-
"""最終的なExcelファイルを保存"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
import os
import re

# 抽出結果のログから企業情報を再構築
# extract_v3_full.txt からデータを読み取る（cp932で試す）
with open('extract_v3_full.txt', 'r', encoding='utf-8-sig') as f:
    content = f.read()

lines = content.split('\n')
companies = []
current = None

for line in lines:
    m = re.match(r'^(\d+)\.\s+(.+)', line)
    if m:
        if current:
            companies.append(current)
        current = {'name': m.group(2), 'business': '', 'address': '', 'email': '', 'website': ''}
    elif current:
        stripped = line.strip()
        if stripped.startswith('事業:'):
            current['business'] = stripped[3:].strip()
        elif stripped.startswith('住所:'):
            current['address'] = stripped[3:].strip()
        elif stripped.startswith('メール:'):
            current['email'] = stripped[4:].strip()
        elif stripped.startswith('URL:'):
            current['website'] = stripped[4:].strip()

if current:
    companies.append(current)

print(f"抽出された企業数: {len(companies)}")

# Byobuの抽出結果部分のみを使用（=== 抽出結果 === 以降）
# 実際のデータはログの累計行までがscrape_allの結果
# print_summary部分は抽出されていないので、累計行のデータを使用
with open('extract_v3_full.txt', 'r', encoding='utf-8-sig') as f:
    raw = f.read()

# scrape_allの累計から企業数を取得
total_match = re.search(r'合計 (\d+) 件の企業情報を取得しました', raw)
total_companies = int(total_match.group(1)) if total_match else 0
print(f"ログ上の合計企業数: {total_companies}")

output_path = u"c:\\Users\\long\\OneDrive\\Code\\Mail\\ホーチミン企業リスト_全1403社.xlsx"

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

for idx, company in enumerate(companies, 1):
    ws.append([
        idx,
        company["name"],
        company["business"],
        company["address"] if company["address"] and company["address"] != "（未取得）" else "",
        company["email"] if company["email"] and company["email"] != "（未取得）" else "",
        company["website"]
    ])

ws.column_dimensions['A'].width = 5
ws.column_dimensions['B'].width = 30
ws.column_dimensions['C'].width = 45
ws.column_dimensions['D'].width = 35
ws.column_dimensions['E'].width = 28
ws.column_dimensions['F'].width = 65

for row in ws.iter_rows(min_row=2, max_row=len(companies)+1):
    for cell in row:
        cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        cell.font = Font(size=10)

wb.save(output_path)
print(f"[成功] ファイルを作成しました: {output_path}")
print(f"[成功] 合計 {len(companies)} 社の情報を記録しました")

with_email = sum(1 for c in companies if c['email'] and c['email'] != '（未取得）' and '@' in c['email'])
print(f"[統計] メールアドレス取得済み: {with_email}/{len(companies)} 社 ({with_email*100//len(companies)}%)")