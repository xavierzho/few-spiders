#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
from lxml import etree


def join_url():
    url_list = []
    for i in range(10):
        url = 'https://maoyan.com/board/4?offset={}'.format(i * 10)
        url_list.append(url)
        # print('正在爬取：{}'.format(url))
    return url_list


def download(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers)
        tree = etree.HTML(r.content.decode())

        if r.status_code == 200:
            films = tree.xpath('//dl[@class="board-wrapper"]/dd')

            for item in films:
                score1 = item.xpath('./div/div[@class="board-item-content"]/div[2]/p/i/text()')[0]
                score2 = item.xpath('./div/div[@class="board-item-content"]/div[2]/p/i[2]/text()')[0]

                info_dict = {
                    'rank': item.xpath('./i/text()')[0],
                    'film_name': item.xpath('./div/div[@class="board-item-content"]/div/p/a/text()')[0],
                    'actor': item.xpath('./div/div[@class="board-item-content"]/div/p[2]/text()')[0].strip()[3:],
                    'release_time': item.xpath('./div/div[@class="board-item-content"]/div/p[3]/text()')[0][5:],
                    'total_score': score1 + score2
                }
                print(info_dict)
                file_path = open('C:/Users/Desire/Downloads/PearVideo/maoyantop100.json', 'a', encoding='utf-8')
                json.dump(info_dict, file_path)
                file_path.close()
        else:
            print(r.status_code)
    except Exception as e:
        print(e)


for ite in join_url():

    download(ite)

