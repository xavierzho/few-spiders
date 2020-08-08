import requests
import json
import time
from lxml import etree


class HuYaLive(object):
    def __init__(self):
        self.classification_url = 'https://www.huya.com/g'
        self.anchor_url = 'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&gameId={}&tagAll=0&page={}'
        self.headers = {
            'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/84.0.4147.105 Safari/537.36'
        }

    # 获取该平台所有的板块
    def get_game_list(self):
        r = requests.get(self.classification_url, headers=self.headers)
        tree = etree.HTML(r.text)
        game_info = tree.xpath('//li[@class="g-gameCard-item"]')
        game_info_list = []
        for item in game_info:
            # //*[@id="js-game-list"]/li[2]/a/p
            game_info_dict = {
                'game_name': item.xpath('./a/p[@class="g-gameCard-fullName"]/text()')[0],
                'game_id': item.xpath('./a/@data-gid')[0],
                'game_url': item.xpath('./a/@href')[0]
            }
            game_info_list.append(game_info_dict)
        # print(game_info_list)
        return game_info_list

    # 拼接板块中每一页的url
    def get_classification_url(self, game_name):
        # 获取参数gameId
        global page, live_url, game_id
        for item in self.get_game_list():
            if item['game_name'] == game_name:
                game_id = item['game_id']
                live_url = item['game_url']
        # 获取参数page
        r = requests.get(live_url, headers=self.headers)
        tree = etree.HTML(r.text)
        pages = tree.xpath('//div[@class="list-page"]/@data-pages')
        u_list = []
        for page in pages:
            for i in range(1, eval(page) + 1):
                # return
                u_list.append(self.anchor_url.format(game_id, i))
        return u_list

    # 找到接口并解json数据，提取所需内容
    def get_anchor_info(self, anchor_info_url):
        html = requests.get(anchor_info_url)
        anchor_json = json.loads(html.text)

        anchor_list = anchor_json['data']['datas']
        # print(res)
        for item in anchor_list:
            anchor_info = {
                'anchor_name': item['nick'],
                'count_popularity': item['totalCount'],
                'room_id': item['profileRoom'],
                'room_name': item['roomName'],
                'introduction': item['introduction']
            }
            print(anchor_info)

    def save_data(self, data):
        with open('anchorInfo.json', 'a') as f:
            f.write(data)

    def main(self):
        live_plate = input('输入直播板块名')
        url_list = self.get_classification_url(live_plate)
        for url in url_list:
            print(url)
            time.sleep(5)
            self.save_data(self.get_anchor_info(url))


if __name__ == '__main__':
    HuYaLive().main()
