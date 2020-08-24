import requests
import base64
import re
from fontTools.ttLib import TTFont
from io import BytesIO
from lxml import etree


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}


def get_html(url):

    response = requests.get(url, headers=headers)
    return response.text


def decode(html):
    bs64_str = re.findall('charset=utf-8;base64,(.*?)\'', html)[0]
    # print(bs64_str)
    # 将base64的字符串转换成二进制
    bin_data = base64.decodebytes(bs64_str.encode())
    # 读取字体二进制文件
    font = TTFont(BytesIO(bin_data))
    # 保存二进制文件
    with open('AnJuKe.otf', 'wb') as f:
        f.write(bin_data)

    # 将字体转化为xml文件
    font.saveXML('AnJuKe.xml')
    # 获取对应的映射关系
    best_map = font['cmap'].getBestCmap()
    # print(best_map)
    # 将字典键转化为16进制
    new_best_map = {}
    for key, value in best_map.items():
        new_best_map[hex(key)] = value
    # print(new_best_map)

    new_map = {
        'glyph00001': '0',
        'glyph00002': '1',
        'glyph00003': '2',
        'glyph00004': '3',
        'glyph00005': '4',
        'glyph00006': '5',
        'glyph00007': '6',
        'glyph00008': '7',
        'glyph00009': '8',
        'glyph00010': '9'
    }
    new_data = {}
    for key, value in new_best_map.items():
        new_data[key] = new_map[value]

    # print(new_data)
    res = {}
    for key, value in new_data.items():
        res['&#' + key[1:] + ';'] = value

    html = html
    for k, v in res.items():
        if k in html:
            # print(k)
            html = html.replace(k, v)
            # print(html)
            # return html

    # def parse_data(html):
    tree = etree.HTML(html)
    data_list = tree.xpath('//div[@class="zu-itemmod"]')
    # print(data_list)
    for data in data_list:
        title = data.xpath('./div[@class="zu-info"]/h3/a/b/text()')[0]
        unit_type_list = data.xpath('./div[@class="zu-info"]/p/b/text()')
        unit_type = unit_type_list[0] + '室' + unit_type_list[1] + '厅' + unit_type_list[2] + '平米'
        area = data.xpath('./div[@class="zu-info"]/address/text()')[1].strip()
        price = data.xpath('./div[@class="zu-side"]/p/strong/b/text()')[0] + '元/月'
        zu_info = ','.join([title, unit_type, area, price])
        print(zu_info)
        # return zu_info


def save_data(data):
    with open('AnJuKe.text', mode='a') as f:
        f.write(data)


if __name__ == '__main__':
    urls_list = ['https://gz.zu.anjuke.com/fangyuan/fanyu/{}/'.format(i) for i in range(1, 11)]
    for url in urls_list:
        decode(get_html(url))

