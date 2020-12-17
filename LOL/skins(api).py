import requests
import json
import pymongo
import copy
# 英雄列表
hero_list = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js'
# 英雄详情
detail_base = "https://game.gtimg.cn/images/lol/act/img/js/hero/%(hero_id)s.js"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}


def response(url):
    resp = requests.get(url, headers=headers)
    return resp


def get_hero_list():
    hero_info = {}
    resp = response(hero_list).text
    data_obj = json.loads(resp)
    hero_info['version'] = data_obj['version']
    hero_info['published'] = data_obj['fileTime']
    for data in data_obj['hero']:
        hero_info['hero_id'] = data['heroId']
        hero_info['hero_name'] = data['name']
        hero_info['hero_title'] = data['title']
        hero_info['hero_link'] = detail_base % {'hero_id': data['heroId']}
        hero_info['alias'] = data['alias']
        yield hero_info


def get_detail():
    for hero in get_hero_list():
        # print(hero['hero_link'])
        resp = response(hero['hero_link']).text
        data_obj = json.loads(resp)
        skins = []
        skin_dict = {}
        skin_list = data_obj['skins']

        for skin in skin_list:
            skin_dict['skin_id'] = skin['skinId']
            if skin['iconImg']:
                skin_dict['icon'] = response(skin['iconImg']).content
            if skin['mainImg']:

                skin_dict['big_img'] = response(skin['mainImg']).content
            if skin['loadingImg']:
                skin_dict['loading_img'] = response(skin['loadingImg']).content
            if not skin['iconImg'] and skin['mainImg'] and skin['loadingImg']:
                if skin['chromaImg']:
                    skin_dict['chromaImg'] = response(skin['chromaImg']).content
            else:
                skin_dict['chromaImg'] = ''
            skin_dict['skin_name'] = skin['name']
            skins.append(skin_dict)
        hero['skins'] = skins

        yield hero


def save():
    client = pymongo.MongoClient(host='localhost', port=27017)
    collection = client['lol']['hero_skin']
    for i in get_detail():
        try:
            collection.insert_one(copy.deepcopy(i))
        except:
            print(i['hero_id'])
    client.close()


if __name__ == '__main__':
    # get_detail()
    save()
