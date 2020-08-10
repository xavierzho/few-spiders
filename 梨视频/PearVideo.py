#!/usr/bin/python
# -*- coding: utf-8 -*-

from requests import get
from re import findall
from selenium import webdriver


option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(
    executable_path='D:/Devtools/ChromeDriver/chromedriver.exe',  # 浏览器driver所在的绝对路径
    options=option
)

start_url = 'https://www.pearvideo.com/category_8'
driver.get(start_url)
print(driver.title)


# 通过webdriver自动加载页面内容，并返回所有详情页url
def join_url():
    for i in range(100):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight); "
                              "var lenOfPage=document.body.scrollHeight; return lenOfPage")
        driver.find_element_by_xpath('//*[@id="listLoadMore"]').click()
        lis = driver.find_elements_by_xpath('//div[@class="vervideo-bd"]/a')
        if driver.find_element_by_xpath('//*[@id="listLoadMore"]').text == '没有更多内容':
            driver.quit()
            break
        yield lis


def enter_page(url):
    for item in url:
        video_url = item.get_attribute('href')
        r = get(video_url)
        download_url = findall('srcUrl="(.*)",vdoUrl=srcUrl', r.text)[0]
        title = findall('<h1 class="video-tt">(.*)</h1>', r.text)[0]
        yield download_url, title


def download(data):
    for it in data:
        print('正在下载：', it[0])
        response = get(it[0])
        with open('C:/Users/Desire/Downloads/PearVideo/{}.mp4'.format(it[1]), 'wb') as f:
            f.write(response.content)


if __name__ == '__main__':
    for ite in join_url():
        download(enter_page(ite))


