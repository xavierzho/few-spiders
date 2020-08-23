#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from lxml import etree


class AmazonSpider:
    def __init__(self):
        self.start_url = 'https://www.amazon.cn/b?node=106200071'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                      '(KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

    def get_url_list(self):
        url_list = ['https://www.amazon.cn/s?rh=n%3A42689071%2Cn%3A%2142690071%2Cn%3A106200071'
                    '&page={}&qid=1598180183&ref=lp_106200071_pg_2 '.format(i) for i in range(2, 101)]
        return url_list

    def get_html_text(self, url):
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            return r.text
        else:
            print(r.status_code)

    def parse_first_page(self):
        response = requests.get(self.start_url, headers=self.headers)
        if response.status_code == 200:
            tree = etree.HTML(response.content.decode())
            data_list = tree.xpath('//ul/li[contains(@class,"result")]')
            for data in data_list:
                product_name = data.xpath('./div/div[3]/div/a/h2/text()')[0]
                product_url = data.xpath('./div/div[3]/div/a/@href')[0]
                product_image = data.xpath('./div/div[2]/div/div/a/img/@src')[0]
                product_price = data.xpath('./div/div[5]/div/a/span[2]/text()')[0]
                product_info = ','.join([product_name, product_image, product_price, product_url])
                return product_info

    def parse_other_pages(self, html):
        tree = etree.HTML(html)
        data_list = tree.xpath('//div[contains(@class, "s-result-item")]')
        try:
            for data in data_list:
                product_name = data.xpath('./div/span/div/div/div[2]/h2/a/span/text()')[0]
                product_url = 'https://www.amazon.cn' + data.xpath('./div/span/div/div/div[2]/h2/a/@href')[0]
                product_image = data.xpath('./div/span/div/div/span/a/div/img/@src')[0]
                product_price = data.xpath('./div/span/div/div/div[3]/div/div/a/span/span[1]/text()|'
                                           './div/span/div/div/div[4]/div/div/a/span/span[1]/text()')[0]
                product_info = ','.join((product_name, product_image, product_price, product_url))
                # print(product_name, product_image, product_price, product_url)
                print(product_info)
        except Exception as e:
            print(e)

    def save_data(self, data):
        pass

    def main(self):
        # self.parse_first_page()
        url_list = self.get_url_list()
        for url in url_list:
            html = self.get_html_text(url)
            self.parse_other_pages(html)


if __name__ == '__main__':
    AmazonSpider().main()
