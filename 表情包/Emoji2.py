import requests
import re
from lxml import etree

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }


def join_url():
    for i in range(1, 2):  # 可调整需要下载页数
        url = 'https://www.fabiaoqing.com/biaoqing/lists/page/{}.html'.format(i)
        yield url


def download(url):
    r = requests.get(url, headers=headers)

    tree = etree.HTML(r.text)
    images = tree.xpath('//div[@class="tagbqppdiv"]')

    for image in images:
        image_url = image.xpath('./a/img/@data-original')[0]

        title = image.xpath('./a/img/@title')[0]

        file_name = title[:10] + image_url[-4:]
        res = re.findall('[\u4e00-\u9fa5a-zA-z0-9]+', file_name, re.S)
        final_name = "".join(res)

        response = requests.get(image_url, headers=headers)

        with open('C:/Users/Desire/Pictures/Camera Roll/{}'.format(final_name), 'wb') as f:
            f.write(response.content)


for item in join_url():
    download(item)

