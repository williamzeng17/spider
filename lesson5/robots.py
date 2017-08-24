# coding: utf-8
"""
版权所有，保留所有权利，非书面许可，不得用于任何商业场景
版权事宜请联系：WilliamZeng2017@outlook.com
"""

import robotparser

rp = robotparser.RobotFileParser()
rp.set_url(url='https://www.baidu.com/robots.txt')
rp.read()
url1 = 'https://www.baidu.com/link?url=123.com'
url2 = 'https://www.baidu.com/home/user/data'
ua = 'Baiduspider'
res1 = rp.can_fetch(ua, url1)
res2 = rp.can_fetch(ua, url2)
print res1, ', ', res2

# True: 允许爬取
# False：不允许爬取



