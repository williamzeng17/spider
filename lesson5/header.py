# coding: utf-8
"""
版权所有，保留所有权利，非书面许可，不得用于任何商业场景
版权事宜请联系：WilliamZeng2017@outlook.com
"""

import requests
from bs4 import BeautifulSoup

session = requests.Session()
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,it;q=0.4,ja;q=0.2,zh-TW;q=0.2",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3188.2 Safari/537.36",
}

url = 'https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending'
objRes = session.get(url, headers=headers)
soup = BeautifulSoup(objRes.text, "html.parser")
print soup.find('table', {'class': 'table-striped'}).text

