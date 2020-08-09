#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(
    executable_path='D:/Devtools/ChromeDriver/chromedriver.exe',  # 浏览器driver所在的绝对路径
    chrome_options=option
)

url = 'https://www.pearvideo.com/category_8'
driver.get(url)
print(driver.title)
# print(driver.page_source)
# title = WebDriverWait(driver, timeout=5).
# until(lambda a: a.find_elements_by_xpath('//li[@class="categoryem"]/div/a/div[2]'))
# href = WebDriverWait(driver, timeout=5).until(lambda a: a.find_elements_by_xpath('//li[@class="categoryem"]/div/a'))
# for item in href:
#     print(item.get_attribute('href'))
# for item in title:
#     print(item.text)
# r = requests.get(url)
# # print(r.text)
tree = etree.HTML(driver.page_source)
lis = tree.xpath('//li[@class="categoryem"]')
for item in lis:
    info_dict = {
        'video_url': item.xpath('./div/a/@href')[0],
        'video_title': item.xpath('./div/a/div[2]/text()')[0]
    }
    print(info_dict)


