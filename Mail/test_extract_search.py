# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import urllib.parse

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
}

session = requests.Session()
r = session.get(
    'https://www.fact-link.com.vn/search_result.php?id=003&type=prov&start=0&lang=jp',
    headers=headers,
    timeout=60
)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.content, 'html.parser')

count = 0
results = []
for span in soup.select('span.default_head'):
    a_tag = span.find('a')
    if a_tag:
        name = a_tag.get_text(strip=True)
        href = a_tag.get('href')
        # Make full URL
        if href.startswith('mem'):
            full_url = 'https://www.fact-link.com.vn/' + href
        else:
            full_url = href
        # Get business description from the td
        td = a_tag.find_parent('td')
        full_text = td.get_text(strip=True) if td else ''
        biz = full_text.replace(name, '', 1).strip()
        results.append((name, biz, full_url))
        count += 1

print(f"Total companies found: {count}")
print("=" * 60)
for i, (n, b, u) in enumerate(results[:10], 1):
    print(f"{i}. {n}")
    print(f"   事業: {b[:100]}")
    print(f"   URL: {u}")
    print()