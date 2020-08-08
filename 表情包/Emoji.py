import requests
import parsel
import os

dir_name = 'imgaes'
if not os.path.exists(dir_name):
    os.mkdir(dir_name)
    # 切换工作目录
    os.chdir(dir_name)
else:
    os.chdir(dir_name)

for page in range(1, 201):
    # 请求服务器
    response = requests.get("https://www.fabiaoqing.com/biaoqing")

# html 前端网页
html = response.text
print(html)
"""在html 里面提取图片地址"""
# 正则表达式（兼容性） Xpath   css选择器
# re lxml.     pyquery


# css选择器 前端
sel = parsel.Selector(html)
# ：伪类选择器  ：：属性选择器   .类选择器
img_s = sel.css('#bqd > div.ui.segment.imghover div > a >img')
# 二次提取
for img in img_s:
    # 提取url属性
    url = img.css('img::attr(data-original)').extract_first()
    # 提取名字属性
    name = img.css('img::attr(title').extract_first()
    print(url, name)

    """下载图片并保存"""

    # 获取后缀名
    suffix = url.split('.gif')[-1]
    # 保存(请求图片)
    response = requests.get('url')
    # 图片 视频 音频 二进制
    try:
        with open(name + '.' + suffix, mode='wb') as f:
            f.write(response.content)
    except OSError as e:
        print(e)
