import requests
import re
import pprint  # 格式化输出内容

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3941.4 Safari/537.36'
}


# 下载一个音频
def download_media(media_url, media_name):
    response = requests.get(media_url)
    print(response)

    with open(media_name + '.mp3', mode='wb') as f:
        f.write(response.content)


# download_media('https://fdfs.xmcdn.com/group11/M00/68/60/wKgDbVcp__Hjsvd2AKLI6upe5iI889.m4a')
"""真实的下载地址"""


def get_media_url_api(id_):
    api_url = 'https://www.ximalaya.com/revision/play/v1/audio?id='+str(id_)+'&ptype=1'

    response = requests.get(api_url, headers=headers
    )
    data = response.json()
    src = data['data']['src']
    return src


"""批量下载"""


response = requests.get('https://www.ximalaya.com/youshengshu/4154350/15287541',headers=headers)
name_id_s = re.findall('<div class="text _c2"><a title="(.*?)" href="/youshengshu/4154350/(.*?)">')

for name, id in name_id_s:

    # id 自动获取到的
    src = get_media_url_api()

print(src)
# 想下载应该是url + name
download_media(src, '章节名字')
