# coding: utf-8
"""
版权所有，保留所有权利，非书面许可，不得用于任何商业场景
版权事宜请联系：WilliamZeng2017@outlook.com
"""

import os
import time
import datetime
import urllib2
import urlparse
from bs4 import BeautifulSoup  # 用于解析网页中文, 安装： pip install beautifulsoup4
from paperDao import PaperDao


def download(url, retry=2):
    """
    下载页面的函数，会下载完整的页面信息
    :param url: 要下载的url
    :param retry: 重试次数
    :return: 原生html
    """
    print "downloading: ", url
    # 设置header信息，模拟浏览器请求
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
    }
    try:  # 爬取可能会失败，采用try-except方式来捕获处理
        request = urllib2.Request(url, headers=header)  # 设置请求数据
        html = urllib2.urlopen(request).read()  # 抓取url
    except urllib2.URLError as e:  # 异常处理
        print "download error: ", e.reason
        html = None
        if retry > 0:  # 未超过重试次数，可以继续爬取
            if hasattr(e, 'code') and 500 <= e.code < 600:  # 错误码范围，是请求出错才继续重试爬取
                print e.code
                return download(url, retry - 1)
    time.sleep(1)  # 等待1s，避免对服务器造成压力，也避免被服务器屏蔽爬取
    return html


def crawl_list(url):
    """
    爬取文章列表区块
    :param url_seed:
    :param url_root:
    :return:
    """
    html = download(url)  # 下载页面
    if html == None:  # 下载页面为空，表示已爬取到最后
        return

    soup = BeautifulSoup(html, "html.parser")  # 格式化爬取的页面数据
    return soup.find(id='list-container').find('ul', {'class': 'note-list'})  # 文章列表


def crawl_paper_tag(list, url_root):
    """
    获取文章列表详情
    :param list:
    :param url_root:
    :return:
    """
    paperList = []  # 文章属性集 list
    lists = list.find_all('li')
    for paperTag in lists:
        content = paperTag.find('div', {'class': 'content'})
        author = content.find('div', {'class': 'author'}).text.strip()  # 作者
        title = content.find('a', {'class': 'title'}).text.strip()  # 标题
        paperUrl = content.find('a', {'class': 'title'}).get('href').strip()  # 文章地址
        abstract = content.find('p', {'class': 'abstract'}).text.strip()
        # 文章摘要
        pic = content.find('a', {'class': 'wrap-img'})  # 文章缩略图
        if pic is not None:
            pic = pic.find('img', {'class': 'img-blur-done'}).get('src').strip()
            pic = urlparse.urljoin(url_root, pic)
        else:
            pic = ''
        metaRead, metaComment, metaLike, metaReward = 0, 0, 0, 0  # 阅读数，评论数，点赞数，打赏数
        meta1 = content.find('div', {'class': 'meta'}).find_all('a')
        meta2 = content.find('div', {'class': 'meta'}).find_all('span')

        for meta in meta1:
            tagClass = meta.find('i').get('class')
            if 'ic-list-read' in tagClass:
                metaRead = meta.text.strip()
            if 'ic-list-comments' in tagClass:
                metaComment = meta.text.strip()

        for meta in meta2:
            tagClass = meta.find('i').get('class')
            if 'ic-list-like' in tagClass:
                metaLike = meta.text.strip()
            if 'ic-list-money' in tagClass:
                metaReward = meta.text.strip()

        paperAttr = {
            'author': author,
            'title': title,
            'url': urlparse.urljoin(url_root, paperUrl),
            'abstract': abstract,
            'content': '',
            'pic': pic,
            'read_cnt': metaRead,
            'comment_cnt': metaComment,
            'like_cnt': metaLike,
            'reward_cnt': metaReward,
        }
        paperList.append(paperAttr)
    return paperList


def crawled_links(url_seed, url_root):
    """
    抓取文章链接
    :param url_seed: 下载的种子页面地址
    :param url_root: 爬取网站的根目录
    :return: 需要爬取的页面
    """
    crawled_url = set()  # 需要爬取的页面
    page = 1
    flag = True  # 标记是否需要继续爬取
    while flag:
        url = url_seed % page  # 真正爬取的页面
        page += 1  # 下一次需要爬取的页面

        html = download(url)  # 下载页面
        if html == None:  # 下载页面为空，表示已爬取到最后
            break

        soup = BeautifulSoup(html, "html.parser")  # 格式化爬取的页面数据
        links = soup.find_all('a', {'class': 'title'})  # 获取标题元素
        if links.__len__() == 0:  # 爬取的页面中已无有效数据，终止爬取
            flag = False

        for link in links:  # 获取有效的文章地址
            link = link.get('href')
            if link not in crawled_url:
                realUrl = urlparse.urljoin(url_root, link)
                crawled_url.add(realUrl)  # 记录未重复的需要爬取的页面
            else:
                print 'end'
                flag = False  # 结束抓取

    paper_num = crawled_url.__len__()
    print 'total paper num: ', paper_num
    return crawled_url


def crawled_page(crawled_url):
    """
    爬取文章内容
    :param crawled_url: 需要爬取的页面地址集合
    """
    for link in crawled_url:  # 按地址逐篇文章爬取
        html = download(link)
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find('h1', {'class': 'title'}).text  # 获取文章标题
        content = soup.find('div', {'class': 'show-content'}).text  # 获取文章内容

        if os.path.exists('spider_res/') == False:  # 检查保存文件的地址
            os.mkdir('spider_res')

        file_name = 'spider_res/' + title + '.txt'  # 设置要保存的文件名
        if os.path.exists(file_name):
            # os.remove(file_name) # 删除文件
            continue  # 已存在的文件不再写
        file = open('spider_res/' + title + '.txt', 'wb')  # 写文件
        content = unicode(content).encode('utf-8', errors='ignore')
        file.write(content)
        file.close()


def save_data(paperList):
    dbPaper = PaperDao()
    for paper in paperList:
        dbPaper.insertOne(paper)


url_root = 'http://www.jianshu.com/'  # 网站根目录
url_seed = 'http://www.jianshu.com/c/9b4685b6357c?page=%d'  # 要爬取的页面地址模板

paperList = crawl_list('http://www.jianshu.com/c/9b4685b6357c?page=1')
paperAll = crawl_paper_tag(paperList, url_root)
save_data(paperAll)
exit(-1)
# print paperAll
# exit(-1)

crawled_url = crawled_links(url_seed, url_root)
crawled_page(crawled_url)
