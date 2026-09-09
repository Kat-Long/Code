# -*- coding: utf-8 -*-
"""
FactLink Vietnam ホーチミン企業情報抽出スクリプト
既知の企業情報から Excel ファイルを生成
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
import os

# 抽出した企業情報（ホーチミンオフィスあり）
companies_data = [
    {
        "name": "ファクトリンクマーケットプレイス有限会社",
        "business": "製造業ポータルサイト「ファクトリンク ベトナム」、工具通販「Fact-Depot」、工業用不動産紹介、ベトナムでの加工部品調達",
        "address": "602/43 Dien Bien Phu Street, Thanh My Tay Ward, Ho Chi Minh City",
        "email": "info@fact-link.com.vn",
        "website": "https://www.fact-link.com.vn/mem_profile.php?id=00051428&page=00005096&lang=jp"
    },
    {
        "name": "ケーティーシー ベトナム 株式会社 KTC (VIETNAM)",
        "business": "精密ゴム成形、自動車用ゴム部品、オートバイ用ゴム部品、OAゴムローラ、携帯電話用ゴム部品、B練り製造",
        "address": "Tan Thuan EPZ LOT BI 22B-24A, 8 STREET, TAN THUAN E.P.Z, TAN THUAN WARD Ho Chi Minh City",
        "email": "ktc-001@ktc-vn.vn",
        "website": "https://www.fact-link.com.vn/mem_profile.php?id=00000116&page=00000189&lang=jp"
    },
    {
        "name": "永大化工ベトナム",
        "business": "合成樹脂異型押出成形加工の専門メーカー。自動車部品（フロアーマット）・プラスチック製品の製造",
        "address": "Ho Chi Minh City",
        "email": "情報取得必要",
        "website": "https://www.fact-link.com.vn/mem_profile.php?id=00000201&page=00000276&lang=jp"
    },
    {
        "name": "株式会社 アキバコーティング ＆ テクノロジー ベトナム",
        "business": "金属表面処理めっき加工、絶縁専門電着塗装",
        "address": "Ho Chi Minh City",
        "email": "情報取得必要",
        "website": "https://www.fact-link.com.vn/mem_profile.php?id=00000295&page=00000369&lang=jp"
    },
    {
        "name": "SG 佐川ベトナム有限会社",
        "business": "国内・国際引越し・国内輸送事業、倉庫業、フォワーディング事業、通関業、貨物検定業",
        "address": "Ho Chi Minh City",
        "email": "情報取得必要",
        "website": "https://www.fact-link.com.vn/mem_profile.php?id=00000823&page=00000958&lang=jp"
    },
    {
        "name": "サトーベトナムソリューションズ",
        "business": "ベトナムでRFID技術、バーコード、ラベル、アプリケーションソリューション",
        "address": "Ho Chi Minh City",
        "email": "情報取得必要",
        "website": "https://www.fact-link.com.vn/mem_profile.php?id=00000858&page=00001029&lang=jp"
    },
    {
        "name": "オリスター株式会社",
        "business": "ベトナムにおける非鉄金属業界のリーディングサプライヤー",
        "address": "Ho Chi Minh City",
        "email": "情報取得必要",
        "website": "https://www.fact-link.com.vn/mem_profile.php?id=00001107&page=00001476&lang=jp"
    },
    {
        "name": "五十鈴テック ベトナム",
        "business": "FAテクノロジーの可能性に挑戦、自動化ニーズの最適化、産業用装置の企画・設計・製作・調整",
        "address": "Ho Chi Minh City",
        "email": "情報取得必要",
        "website": "https://www.fact-link.com.vn/mem_profile.php?id=00001221&page=00001715&lang=jp"
    },
    {
        "name": "QUANG NGHI SERVICE AND TRADING-PRODUCT COMPANY LIMITED",
        "business": "乾燥剤（シリカゲル）、防湿パッケージの製造と販売、カビ防止ソリューション",
        "address": "Ho Chi Minh City",
        "email": "情報取得必要",
        "website": "https://www.fact-link.com.vn/mem_profile.php?id=00001975&page=00002693&lang=jp"
    },
    {
        "name": "タイコー ベトナム",
        "business": "金属加工、樹脂加工、アッセンブリー",
        "address": "Ho Chi Minh City",
        "email": "情報取得必要",
        "website": "https://www.fact-link.com.vn/mem_profile.php?id=00002045&page=00002769&lang=jp"
    },
    {
        "name": "ジーケー・ファインケム ベトナム",
        "business": "化学品（試薬・高純度薬品・工業用基礎薬品・工業用溶剤）の輸入販売",
        "address": "Ho Chi Minh City",
        "email": "情報取得必要",
        "website": "https://www.fact-link.com.vn/mem_profile.php?id=00002487&page=00003184&lang=jp"
    },
    {
        "name": "クイックベトナム",
        "business": "採用・人事部門サポート、日本人紹介、ベトナム人紹介",
        "address": "Ho Chi Minh City",
        "email": "情報取得必要",
        "website": "https://www.fact-link.com.vn/mem_profile.php?id=00051537&page=00005139&lang=jp"
    }
]

def create_excel_file(companies, output_path=None):
    """Excelファイルを作成"""
    if output_path is None:
        output_path = u"c:\\Users\\long\\OneDrive\\Code\\Mail\\ホーチミン企業リスト.xlsx"
    
    # 既存ファイルを削除
    if os.path.exists(output_path):
        try:
            os.remove(output_path)
            print(u"既存ファイルを削除しました")
        except Exception as e:
            print(u"既存ファイルの削除に失敗: {}".format(str(e)))
            return False
    
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = u"ホーチミン企業リスト"
        
        # ヘッダー行の設定
        headers = [u"No.", u"社名", u"事業内容", u"住所", u"メール", u"FactLinkベトナムウェブサイト"]
        ws.append(headers)
        
        # ヘッダーのスタイル設定
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF", size=11)
        
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
        # データ行の追加
        for idx, company in enumerate(companies, 1):
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
        
        # セルのスタイル設定
        for row in ws.iter_rows(min_row=2, max_row=len(companies)+1):
            for cell in row:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
                cell.font = Font(size=10)
        
        # ファイルを保存
        wb.save(output_path)
        print(u"[成功] ファイルが作成されました")
        print(u"[成功] 合計 {} 社の情報を記録しました".format(len(companies)))
        print(u"[成功] 出力先: {}".format(output_path))
        return True
    except Exception as e:
        print(u"[エラー] ファイル作成に失敗: {}".format(str(e)))
        return False

if __name__ == "__main__":
    print(u"ホーチミン企業リスト生成スクリプトを開始します")
    print(u"-" * 50)
    
    success = create_excel_file(companies_data)
    
    if success:
        print(u"\n=== 抽出結果サマリー ===")
        print(u"合計企業数: {}".format(len(companies_data)))
        print(u"\n登録企業:")
        for idx, company in enumerate(companies_data, 1):
            print(u"  {}. {} ({})".format(idx, company['name'], company['address']))
