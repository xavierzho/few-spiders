from multiprocessing import pool
import requests
import random
import os


# 电影地址url通过http://czjx8.com/解析出url下载地址
def downvideo():
    agent1 = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3732.400 QQBrowser/10.5.3819.400 "}
    agent2 = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"}
    agent3 = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"}
    list1 = [agent1, agent2, agent3]
    agent = random.choice(list1)
    for x in range(157):
        # ts文件数量
        if 0 < x < 10:
            url = 'https://youku.cdn7-okzy.com/20191103/15625_390b034f/1000k/hls/254052297ef000155/film_0000' + str(
                x) + ".ts"
        elif 9 < x < 100:
            url = "https://youku.cdn7-okzy.com/20191103/15625_390b034f/1000k/hls/254052297ef000155/film_000" + str(
                x) + ".ts"
        elif 100 <= x < 1000:
            url = "https://youku.cdn7-okzy.com/20191103/15625_390b034f/1000k/hls/254052297ef000155/film_00" + str(
                x) + ".ts"
        elif x >= 1000:
            url = "https://youku.cdn7-okzy.com/20191103/15625_390b034f/1000k/hls/254052297ef000155/film_0" + str(
                x) + ".ts"

        try:
            response = requests.get(url, headers=agent)
            response.encoding = response.apparent_encoding
            html = response.content
            path = "E://movie//"
            if not os.path.exists(path):
                os.mkdir(path)
            abspath = path + str(x) + ".ts"
            with open(abspath, "wb") as f:
                f.write(html)
                f.close()
                print("{}下载完成", format(url))

        except:
            print("爬取失败")
            continue


if __name__ == "__main__":
    downvideo()
