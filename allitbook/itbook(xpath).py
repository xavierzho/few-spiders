import requests
import json
from lxml import etree


class BookSpider(object):
    def __init__(self):
        self.base_url = 'http://www.allitebooks.org/page/{}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }
        self.data_list = []

    def send_request(self, url):
        data = requests.get(url, headers=self.headers).content.decode()
        return data

    def get_url_list(self):
        url_list = []
        # 遍历url
        for i in range(1, 861):
            url = self.base_url.format(i)
            url_list.append(url)

        return url_list

    def parse_one_page_data(self, data):
        parse_data = etree.HTML(data)
        book_list = parse_data.xpath("//div[@class='entry-thumbnail hover-thumb']")

        # 解析出每本书信息
        for book in book_list:
            for i in range(10):
                book_dict = {'book_name': book.xpath("//h2[@class='entry-title']/a/text()")[i],
                             'book_url': book.xpath("//h2[@class='entry-title']/a/@href")[i],
                             'book_author': book.xpath("//h5[@class='entry-author']/a/text()")[i],
                             'book_introduction': book.xpath("//div[@class='entry-summary']/p/text()")[i]
                             }
                self.data_list.append(book_dict)

            return self.data_list

    def save_data(self, data):
        fp = open('itbook.json', 'w', encoding='utf-8')
        json.dump(data, fp)
        fp.close()

    def main(self):

        url_list = self.get_url_list()
        for url in url_list:
            print('正在爬取：{}'.format(url))
            data = self.send_request(url)
            data2 = self.parse_one_page_data(data)
            # self.save_data(data2)


BookSpider().main()
