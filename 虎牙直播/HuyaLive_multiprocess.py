import requests
# from multiprocessing import Pool, Manager
from lxml import etree


class HuYaLive(object):
    def __init__(self):
        self.classification_url = 'https://www.huya.com/g'
        self.page_url = 'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&gameId={}&tagAll=0&page={}'
        self.headers = {
            'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/84.0.4147.105 Safari/537.36'
        }

    def response(self, url):
        r = requests.get(url, hearders=self.headers,)
        if r.status_code == 200:
            return r.text, r.content.decode(), r.json()

    # 获取该平台所有的板块
    def get_plates_list(self):
        html = self.response(self.classification_url)[0]
        tree = etree.HTML(html)
        plates = tree.xpath('//li[@class="g-gameCard-item"]')
        plates_list = []
        for plate in plates:
            plate_dict = {
                'game_name': plate.xpath('./@title')[0],
                'game_id': plate.xpath('./a/@data-gid')[0],
                'game_url': plate.xpath('./a/@href')[0]
            }
            plates_list.append(plate_dict)
        return plates_list

    def join_url(self):
        plates = self.get_plates_list()
        for plate in plates:
            game_id = plate['game_id']
            for i in range():
                url = self.page_url.format(game_id, )
                self.response()

    # 找到接口并解json数据，提取所需内容
    def parse_json_data(self, url):
        data_json = self.response(url)[2]
        anchor_list = data_json['data']['datas']
        for item in anchor_list:
            anchor_info = {
                'anchor_name': item['nick'],
                'count_popularity': item['totalCount'],
                'room_id': item['profileRoom'],
                'room_name': item['roomName'],
                'introduction': item['introduction']
            }
            print(anchor_info)


if __name__ == '__main__':
    # pool = Pool(10)
    pass
