# -*- coding: utf-8 -*-
import re
import scrapy


class HlmSpider(scrapy.Spider):
    name = 'hlm'  # 爬虫名字
    allowed_domains = ['purepen.com']  # 允许采集的域名
    start_urls = ['http://www.purepen.com/index.html']  # 开始采集的网站

    # 解析网站 start_urls 中的返回数据response
    def parse(self, response):
        urls = re.findall(r'<br>.*?<a href="(.*?)">第', response.text, flags=re.S)
        for url in urls:
            # 拼接完整的网址
            url = f'http://www.purepen.com/hlm/{url}'
            # 循环里面需要返回数据一定要用 yield return
        yield scrapy.Request(url, callback=self.parseDetail)

    def parseDetail(self, response):
        result = re.findall('<font size="3">(.*?)</font>', response.text, flags=re.S)
        if result:
            print(result[0])


