# 36氪快讯
import requests
import json
from lxml import etree

header = {
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}

url = 'https://36kr.com/newsflashes'
# url = 'https://gateway.36kr.com/api/mis/nav/newsflash/flow'
response = requests.get(url, headers=header, timeout=5)
# print(response.text)
# result = json.loads(response.text)
tree = etree.HTML(response.text)
items = tree.xpath('//div[@class="newsflash-item"]')
data_list = []
for item in items:
    data_dict = {
        'title': item.xpath('./a/text()'),
        'desc': item.xpath('./div[@class="item-desc"]/span/text()'),
        'original_link': item.xpath('./div[@class="item-desc"]/a/@href')
    }
    data_list.append(data_dict)
print(data_list)
