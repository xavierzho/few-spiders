import requests
import threadpool
import time
import os, sys
import re
from lxml import etree
from lxml.html import tostring


class ScrapDemo():
    next_page_url = ""
    page_num = 1
    detail_url_list = 0
    deepth = 0
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0;Win64;x64)  AppleWebkit/537.36 (KHTML, like Gecko)Chrome/68.0.3440.84 Safari/537.36"}
    fileNum = 0

    def __init__(self, url):
        self.scrapyIndex(url)

    def threadIndex(self, urllist):
        if len(urllist) == 0:
            print("请输入需要爬取的地址")
            return False
        ScrapDemo.detail_url_list = len(urllist)
        pool = threadpool.ThreadPool(len(urllist))
        requests = threadpool.makeRequests(self.detailScray, urllist)
        for req in requests:
            pool.putRequest(req)
            time.sleep(0.5)
            pool.wait()

    def detailScray(self, url):
        if not url == "":
            url = 'http://xiaohua.zol.com.cn/{}'.format(url)
            res = requests.get(url, headers=ScrapDemo.headers)
            html = res.text

            self.downloadText(html)

    def downloadText(self, ele):
        clist = re.findall('<div class=" article-text">(.*?)</div>'.ele, re, 5)
        for index in range(len(clist)):
            clist[index] = re.sub(r'(\r|\t|<p>|<\/p>)+', '', clist[index])
        content = "".join(clist)

        basedir = os.path.dirname(__file__)
        filePath = os.path.join(basedir)
        filename = " xiaohua{0}-{1}.txt".format(ScrapDemo.deepth, str(ScrapDemo.fileNum))
        file = os.path.join(filePath, 'file_txt', filename)
        try:
            f = open(file, "w")
            f.write(content)
            if ScrapDemo.fileNum == (ScrapDemo.detail_url_list - 1):
                print(ScrapDemo.next_page_url)
                print(ScrapDemo.deepth)
                if not ScrapDemo.next_page_url == "":
                    self.scrapyIndex(ScrapDemo.next_page_url)
        except Exception as e:
            print("Error:%s" % str(e))
        ScrapDemo.fileNum = ScrapDemo.fileNum + 1
        print(ScrapDemo.fileNum)

    def scrapyIndex(self, url):
        if not url == "":
            ScrapDemo.fileNum = 0
            ScrapDemo.deepth = ScrapDemo.deepth + 1
            print("开始第{0}页抓取".format(ScrapDemo.page_num))
            res = requests.get(url, headers=ScrapDemo.headers)
            html = res.text
            element = etree.HTML(html)
            a_urllist = element.xpath("//a[@class='all-read']/@href")
            next_page = element.xpath("//a[@class='page-next']/@href")
            ScrapDemo.next_page_url = 'http://xiaohua.zol.com.cn/{}'.format(next_page[0])
            if not len(next_page) == 0 and ScrapDemo.next_page_url != url:
                ScrapDemo.page_num = ScrapDemo.page_num + 1
                self.threadIndex(a_urllist[:])
            else:
                print('下载完成，当前页数为{}页'.format(ScrapDemo.page_num))
