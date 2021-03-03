"""
@Author: Jonescyna@gmail.com
@Created: 2021/1/22
"""
import requests

keyword = '白月光'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63",
}
api = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"
params = {
    'w': keyword,
    'p': 1,
    'n': 10,
    'format': "json"
}
resp = requests.get(api, headers=headers, params=params)
for i in resp.json()['data']['song']['list']:
    print(i)
