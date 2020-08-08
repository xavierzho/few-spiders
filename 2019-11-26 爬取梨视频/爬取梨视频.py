import re
import requests


# 得到网页数据
def download_one_media():
    url = "https://www.pearvideo.com/category_8"
    response = requests.get(url)

    f = open()
    f.write(response.content)
    f.close()


# 命名规范 见名知意
def download_category_page(category_page_url):
    print()
