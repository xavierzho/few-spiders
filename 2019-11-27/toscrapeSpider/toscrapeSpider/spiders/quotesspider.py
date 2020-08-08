# -*- coding: utf-8 -*-
import scrapy


# 基础的类
class QuotesspiderSpider(scrapy.Spider):
    name = 'quotesspider'  # 爬虫名字
    allowed_domains = ['http://quotes.toscrape.com/']  # 只在这个网站下采集
    start_urls = ['http://quotes.toscrape.com/page/{page}/'for page in range(1, 10)]  # 开始采集网站

    # 方法 函数
    def parse(self, response):
        """
        这个函数是用来处理响应的 response 就是下载的数据
        :param response: 就是下载的数据
        :return: 数据 xpath
        """
        # 提取数据
        selectors = response.xpath('//div[@class="col-md-8"]/div')  #
        for selector in selectors:
            text = selector.xpth('.//span[@class="text"]/text()').get()
            print(text)
            # 保存数据
            items ={
                'text': text
            }
            yield items  #
