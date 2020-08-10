# 当当网书评
import json
import requests
from lxml import etree

for i in range(1, 5):
    url = 'http://product.dangdang.com/index.php?r=comment%2Flist&productId=28524517&categoryPath=01.24.01.00.00.00&mainProductId=28524517&mediumId=0&pageIndex={}&sortType=1&filterType=1&isSystem=1&tagId=0&tagFilterCount=0&template=publish'.format(i)
    header = {
            'Accept': 'application/json,text/javascript,*/*;q=0.01',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }
    response = requests.get(url, headers=header, timeout=5)
    result = json.loads(response.text)

    comment_html = result['data']['list']['html']

    tree = etree.HTML(comment_html)
    print(tree)
    comments = tree.xpath('//div[@class="items_right"]')

    # for item in comments:
    #     comment_time = item.xpath('./div[contains(@class,"starline")]/span[1]/text()')[0]
    #     comment_content = item.xpath('./div[contains(@class,"describe_detail")]/span[1]//text()')[0]
    #     print(comment_time)
    #     print(comment_content)
