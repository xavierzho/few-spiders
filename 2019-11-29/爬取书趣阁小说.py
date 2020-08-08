import requests
import re

url = r'http://www.shuquge.com/txt/8659/2324752.html'
response = requests.get(url)
# 设置响应体的编码属性，万能设置编码
response.encoding = response.apparent_encoding

# 打印文字属性
print(response.text)

# 2.解析想要的数据 re css选择器 xpath

