import requests
import re
from lxml import etree


headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }
start_url = 'http://www.shuquge.com/txt/8659/index.html'


def get_chapter_url():
    response = requests.get(start_url, headers=headers)
    # 设置响应体的编码属性，万能设置编码
    response.encoding = response.apparent_encoding

    tree = etree.HTML(response.text)

    # 2.解析想要的数据 re css选择器 xpath
    url_list = tree.xpath('//div[@class="listmain"]/dl/dd/a/@href')[12::]
    chapter_list = []
    for url in url_list:
        chapter_url = 'http://www.shuquge.com/txt/8659/{}'.format(url)
        chapter_list.append(chapter_url)
    return chapter_list


def get_book_content(url):
    r = requests.get(url, headers=headers)
    chapter_tree = etree.HTML(r.content.decode('utf-8'))
    title = chapter_tree.xpath('//div[@class="content"]/h1/text()')[0]
    contents = chapter_tree.xpath('//div[@class="showtxt"]/text()')

    for content in contents:
        print(content)
        with open('C:/Users/Desire/Documents/剑来/{}'.format(title), 'a', encoding='utf-8') as f:
            f.write(content)


def main():
    lis = get_chapter_url()
    for item in lis:
        get_book_content(item)


main()
