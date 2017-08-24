# coding: utf-8
"""
版权所有，保留所有权利，非书面许可，不得用于任何商业场景
版权事宜请联系：WilliamZeng2017@outlook.com
"""

from selenium import webdriver  # pip2 install selenium

driver1 = webdriver.PhantomJS()  # 需下载安装phantomjs：http://phantomjs.org/download.html
# driver1 = webdriver.PhantomJS(executable_path='PATH TO phantomjs.exe')  # windows环境
driver1.get('https://www.baidu.com')
driver1.implicitly_wait(1)

webCookies1 = driver1.get_cookies()  # 获取cookie
print webCookies1

# driver2 = webdriver.Chrome(executable_path='PATH TO chromedriver.exe')  # windows
driver2 = webdriver.Chrome()  # phantomjs2.1.1有点问题，无法设置cookie，所以换成了chromedriver，下载地址：https://sites.google.com/a/chromium.org/chromedriver/home
driver2.get('https://www.baidu.com')
driver2.delete_all_cookies()
for cookie in webCookies1:
    driver2.add_cookie(cookie)  # phantomjs2.1.1有点问题，无法设置cookie
driver2.get('https://www.baidu.com')
driver2.implicitly_wait(1)
webCookies2 = driver2.get_cookies()
print webCookies2

driver1.quit()
driver2.quit()


