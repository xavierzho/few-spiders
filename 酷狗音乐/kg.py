"""
@Author: Jonescyna@gmail.com
@Created: 2021/1/22
"""
import requests
import time
import re


def parse_lyrics(lyrics):
    for line in lyrics.split('\r\n'):
        lyric = line.replace('[', '').split(']')
        if len(lyric) > 1 and lyric[1]:
            print(lyric[1])


keyword = "白月光与朱砂痣"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63",
}
# p = "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt"
api = 'https://songsearch.kugou.com/song_search_v2?keyword={}&page=1&pagesize=100&userid=-1&clientver=&platform=WebFilter&tag=&filter=2&iscorrection=1&privilege_filter=0&_={}'
k = str(time.time_ns())[:13]

resp = requests.get(api.format(keyword, k), headers=headers)
# print(resp.json())
song_list = resp.json()['data']['lists']

for item in song_list[:1]:
    file_hash = item['FileHash']
    album_id = item['AlbumID']
    file_name = item['FileName']+"."+item['ExtName']
    detail_url = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={}&album_id={}&_={}'.format(file_hash, album_id, k)
    headers['sec-ch-ua'] = '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"'
    headers['cookie'] = '__fx_unionId__=148-0; BusinessId={"std_plat":8,"std_dev":"55d0f990-13c3-4d8b-d1bc-d9e574f0f89a","std_imei":"55d0f990-13c3-4d8b-d1bc-d9e574f0f89a","version":0}; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1611277610; kg_mid=3f6f255673dce3c7b467554a7cb4abae; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; kg_dfid=3w4Xoq1IuAtg3dTOJ347oIn4; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1611298498'
    json_text = requests.get(detail_url, headers=headers)
    mp3_url = json_text.json()['data']['play_url']
    lyrics = json_text.json()['data']['lyrics']
    # print(file_name, mp3_url)
    parse_lyrics(lyrics)


