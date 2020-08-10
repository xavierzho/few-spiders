"""抓取QQ音乐巅峰榜单热歌榜
1.找到音乐文件的下载链接
url= 'https://ws.stream.qqmusic.qq.com/C400000LbvRN0WK7Rl.m4a?
guid=277523144&vkey=B96239852D3D2999F40F66EDAEA03A54951BA28FB2044F0FA3DC78A12FFCDB0164AB813F232DBD6DCF293AF6FDF0BDDFC976B3C0199789AA
&uin=3011&fromtag=66'
2.比较不同的歌，分析下载链接的关键词：songmid和vkey
3.寻找vkey在那个响应（过滤vkey）
4.构造请求网站
"""


import requests
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def download_music(song_mid, music_name):
    data = json.dumps({"req": {"module": "CDN.SrfCdnDispatchServer",
                               "method": "GetCdnDispatch",
                               "param": {"guid": "1647290160",
                                         "calltype": 0, "userip": ""}},
                       "req_0": {"module": "vkey.GetVkeyServer",
                                 "method": "CgiGetVkey",
                                 "param": {"guid": "1647290160",
                                           "songmid": [song_mid],
                                           "songtype": [0],
                                           "uin": "1152921504736349123",
                                           "loginflag": 1,
                                           "platform": "20"}},
                       "comm": {"uin": "1152921504736349123",
                                "format": "json",
                                "ct": 24,
                                "cv": 0}})

    url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?callback=getplaysong' \
          'vkey39450380565091747&g_tk=1048458740&jsonpCallback=getplaysong' \
          'vkey39450380565091747&loginUin=1152921504736349123&hostUin=0&' \
          'format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data={}'.format(data)
    html = requests.get(url)
    music_json = json.loads(re.findall(r'^\w+\((.*)\)$', html.text)[0])
    print(music_json)
    filename = music_json['req_0']['data']['midurlinfo'][0]['filename']
    print(filename)
    vkey = music_json['req_0']['data']['midurlinfo'][0]['vkey']
    download_url = 'http://113.105.167.149/amobile.music.tc.qq.com/' \
                   'C400{}.m4a?guid=1647290160&vkey={}&uin=3011&fromtag=66'.format(filename, vkey)
    print(download_url)

    # 下载到本地
    music = requests.get(download_url)
    with open('C:/Users/Desire/Music/QQMusic/{}.m4a'.format(re.sub(r"[\s+|@<>:\\'/]", '', music_name)), 'wb') as m:
        m.write(music.content)


def view_html():
    # QQ音乐页面是js加载的，这里使用chrome headless模式访问
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(
        executable_path='D:/Devtools/ChromeDriver/chromedriver.exe',  # 浏览器driver所在的绝对路径
        chrome_options=option
    )
    driver.get('https://y.qq.com/n/yqq/toplist/26.html')
    print(driver.title)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "songlist__songname_txt")))

        lis = driver.find_elements_by_class_name('songlist__songname_txt')
        pattern = re.compile(r'https://y.qq.com/n/yqq/song/(\S+).html')
        for i in range(lis.__len__()):
            li = lis.__getitem__(i)
            a = li.find_element_by_class_name('js_song')
            # 获取songid
            href = a.get_attribute('href')
            # print(href)
            music_name = a.get_attribute('title')
            print(music_name)
            m = pattern.match(href)
            # print(m.group(1))
            download_music(m.group(1), music_name)
    finally:
        driver.quit()


if __name__ == '__main__':
    view_html()
