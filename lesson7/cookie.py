# coding: utf-8
"""
版权所有，保留所有权利，非书面许可，不得用于任何商业场景
版权事宜请联系：WilliamZeng2017@outlook.com
"""

import urllib2
import lxml.html
import Cookie
import cookielib


def build_opener_with_cookie_str(cookie_str, domain, path='/'):
    simple_cookie = Cookie.SimpleCookie(cookie_str)  # Parse Cookie from str
    cookiejar = cookielib.CookieJar()  # No cookies stored yet

    for c in simple_cookie:
        cookie_item = cookielib.Cookie(
            version=0,
            name=c,
            value=str(simple_cookie[c].value),
            port=None,
            port_specified=None,
            domain=domain,
            domain_specified=None,
            domain_initial_dot=None,
            path=path,
            path_specified=None,
            secure=None,
            expires=None,
            discard=None,
            comment=None,
            comment_url=None,
            rest=None,
            rfc2109=False,
        )
        cookiejar.set_cookie(cookie_item)  # Apply each cookie_item to cookiejar
    return urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))  # Return opener


def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form#loginform input'):
        if e.get('name') and e.get('type') == 'hidden':
            data[e.get('name')] = e.get('value')
    return data


# 设置header
header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,it;q=0.4,ja;q=0.2,zh-TW;q=0.2",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3188.2 Safari/537.36",
}

cookie_str = 'cookie_str'

opener = build_opener_with_cookie_str(cookie_str, 'www.jianshu.com')
html_doc = opener.open('http://www.jianshu.com').read()
print html_doc
