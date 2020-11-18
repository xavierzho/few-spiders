import ssl
import time
from selenium import webdriver
import os
import urllib.request
import re

# 创建有个默认的ssl证书
ssl_create_default_https_context = ssl._create_unverified_context

driver = webdriver.Firefox(executable_path='D://WebDriver/geckodriver.exe',
                           options=webdriver.FirefoxOptions())

hero = []
url = 'https://lol.qq.com/data/info-heros.shtml'


def get_images():
    driver.get(url)
    time.sleep(3)
    driver.execute_script('window.scroll(0,document.body.scrollHeight)')
    element = driver.find_element_by_id("jSearchHeroDiv")
    # print(element.text)
    links = element.find_elements_by_css_selector('li>a')
    for link in links:
        urls = link.get_attribute('href')
        hero.append(urls.split())
    for _ in range(len(hero)):
        # print(hero[_][0])
        driver.get(hero[_][0])
        time.sleep(2)
        # 控制浏览器定位到指定位置
        driver.execute_script('window.scrollTo(100,800)')
        # 抓取一个英雄的所有皮肤
        driver.find_element_by_css_selector("#skinNAV").find_elements_by_css_selector("li a")[1].click()
        #
        # driver.find_element_by_css_selector()
        # 定位大图
        skins = driver.find_elements_by_xpath('//ul[@id="skinBG"]/li')
        for skin in skins:
            pattern = r'[\\/:*?"<>|\r\n]+'
            skin_name = re.sub(pattern, '_', skin.get_attribute('title'))
            skin_img = skin.find_element_by_css_selector('img').get_attribute('src')
            # print(skin_name, skin_img)
            hero_name = driver.find_element_by_xpath('//a[@class="here"]').text.split(' ')[0]
            if not os.path.exists(r'C:\Users\jonescy\Pictures\Saved Pictures\lol\%s' % hero_name):
                os.makedirs(r'C:\Users\jonescy\Pictures\Saved Pictures\lol\%s' % hero_name)
            hero_path = r'C:\Users\jonescy\Pictures\Saved Pictures\lol\%s' % hero_name
            # print(hero_path + '\%s.jpg' % hero_name)
            try:
                if os.path.exists(hero_path):
                    file_name = r'C:\Users\jonescy\Pictures\Saved Pictures\lol\%s\%s' % (hero_name, skin_name)
                    if not os.path.exists(file_name):
                        urllib.request.urlretrieve(skin_img, hero_path + '\%s.jpg' % skin_name)
            except:
                print("无法获取:", skin_img)
                pass


get_images()
