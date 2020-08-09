#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import time
from lxml import etree


class XiMaLaYa(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/79.0.3941.4 Safari/537.36'
        }
        self.book_url = 'https://www.ximalaya.com/youshengshu/3580611/'

    def send_requests(self, url):
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            return r.content.decode()
        else:
            print(Exception)

    def book_introduction(self, html):
        tree = etree.HTML(html)
        introduction = tree.xpath('//div[@class="album-intro aB_"]/article/p/text()')[0]
        return introduction

    def get_chapter_info(self, html):
        tree = etree.HTML(html)
        chapter_url_list = tree.xpath('//div[@class="sound-list _Qp"]/ul/li')
        chapter_list = []
        for item in chapter_url_list:
            chapter_dict = {
                "title": item.xpath('./div[@class="text _Vc"]/a/@title')[0],
                "chapter_id": item.xpath('./div[@class="text _Vc"]/a/@href')[0][-8:]
                          }
            chapter_list.append(chapter_dict)
        # print(chapter_list)
        return chapter_list

    def page_url(self):
        page_list = []
        for i in range(1, 100):
            page_url = self.book_url+'p{}/'.format(i)
            page_list.append(page_url)
        return page_list

    def download_chapter_audio(self, url):
        info_list = self.get_chapter_info(self.send_requests(url))
        # print(info_list)
        count = 0
        global download
        for item in info_list:
            # print(item)
            chapter_id = item['chapter_id']
            # print(chapter_id)
            url = 'https://www.ximalaya.com/revision/play/v1/audio?id={}&ptype=1'.format(chapter_id)
            response = requests.get(url, headers=self.headers)
            download_url = json.loads(response.text)['data']['src']
            count += 1
            print(count, ":", download_url)
            download = requests.get(download_url, headers=self.headers)
        return download

    def save_introduction(self, data):
        with open('C:/Users/Desire/Downloads/audioBook/bookIntroduction.txt', 'w') as f:
            f.write(data)

    def save_media(self, data, url):
        for item in self.get_chapter_info(self.send_requests(url)):
            title = item['title']
            with open('C:/Users/Desire/Downloads/audioBook/{}.m4a'.format(title), 'ab') as f:
                f.write(data.content)

    def main(self):
        for page in self.page_url():
            print(page)
            introduction = self.send_requests(page)
            self.save_media(self.download_chapter_audio(page), page)
            if not self.get_chapter_info(introduction):
                break
            # self.download_chapter_audio()
            # self.save_introduction(self.book_introduction(introduction))


if __name__ == '__main__':
    XiMaLaYa().main()
