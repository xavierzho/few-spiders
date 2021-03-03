"""
@Author: Jonescyna@gmail.com
@Created: 2021/1/22
"""
import requests
from urllib.parse import quote

keyword = "白月光"
api = 'https://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={}&pn=1&rn=30&httpsStatus=1'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63",
    "Cookie": "_ga=GA1.2.1083049585.1590317697; _gid=GA1.2.2053211683.1598526974; _gat=1; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1597491567,1598094297,1598096480,1598526974; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1598526974; kw_token=HYZQI4KPK3P",
    "Referer": quote("http://www.kuwo.cn/search/list?key={}".format(keyword)),
    "csrf": "HYZQI4KPK3P",
}

api_resp = requests.get(api.format(keyword), headers=headers)

