# coding: utf-8
"""
版权所有，保留所有权利，非书面许可，不得用于任何商业场景
版权事宜请联系：WilliamZeng2017@outlook.com
"""

import urllib, urllib2
import cookielib
import lxml.html


def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form#loginform input'):
        if e.get('name') and e.get('type') == 'hidden':
            data[e.get('name')] = e.get('value')
    return data


login_url = 'http://www.ttmeiju.com/index.php/user/login.html'  # 登录地址

# 设置header
header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,it;q=0.4,ja;q=0.2,zh-TW;q=0.2",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3188.2 Safari/537.36",
}

cj = cookielib.CookieJar()  # 创建cookie对象
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
html = opener.open(login_url).read()  # 先加载登录页面
data = parse_form(html)
login_name = 'username'
login_pwd = 'passwd'
data['username'] = login_name
data['password'] = login_pwd
encode_data = urllib.urlencode(data)
request = urllib2.Request(login_url, encode_data, header)  # 必须有header模拟浏览器，否则会返回403 Forbidden
respose = urllib2.urlopen(request)
print respose.geturl()  # 登录之后的页面


