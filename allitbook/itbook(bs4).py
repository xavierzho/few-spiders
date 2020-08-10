import requests
import json
from bs4 import BeautifulSoup


class BookSpider(object):
    def __init__(self):
        self.base_url = 'http://www.allitebooks.org/page/{}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }

    def send_request(self, url):
        data = requests.get(url, headers=self.headers).content.decode()
        return data

    def get_url_list(self):
        url_list = []
        # 遍历url
        for i in range(16, 17):
            url = self.base_url.format(i)
            url_list.append(url)

        return url_list

    def parse_one_page_data(self, data):
        soup = BeautifulSoup(data, 'lxml')
        book_list = soup.select("article")
        data_list = []

        # 解析出每本书信息
        for book in book_list:
            book_dict = {'book_name': book.select_one('.entry-body a').get_text(),
                         'book_url': book.select_one(".entry-body a").get("href"),
                         'book_author': book.select_one(".entry-author a").get_text(),
                         'book_introduction': book.select_one(".entry-summary p").get_text()
                         }
            data_list.append(book_dict)
        return data_list

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
            self.save_data(data2)


BookSpider().main()

