import requests
import re  # 正则表达式模块


# 获取所有的页数
def getAllUrl():
    url = "http://www.purepen.com/jpm/index.htm"
    response = requests.get(url)
    response.encoding = 'gbk'
    # r 转译网页代码  # 本身就是列表
    urls = re.findall(r'<br>.*?<a href="(.*?)">第', response.text, flags=re.S)
    # for url in urls:
    #     # 拼接完整的网址
    #     url = f'http://www.purepen.com/jpm/{url}.htm'
    #     # 循环里面需要返回数据一定要用 yield return
    # yield url
    return [f'http://www.purepen.com/jpm/{url}' for url in urls]


def getDetailPage(url):
    # url = 'http://www.purepen.com/jpm/001.htm'
    # 结果给response
    response = requests.get(url)
    # 解决乱码
    response.encoding = 'gb2312'  # ios-18930>>gbk>>gb2312
    return response.text


def parseDetailPage(text):
    # (.*?)提取任何文本 . 意思只能匹配除了和换行以外的单个字符
    result = re.findall('<font size="3">(.*?)</font>', text, flags=re.S)
    if result:
        pipelines(result[0])


# 保存数据
def pipelines(item):
    with open('金.text', 'a', encoding='utf-8') as fp:
        print(item[:20].strip())  # 空白字符 空格 制表符 换行
        fp.write(item)


if __name__ == '__main__':
    urls = getAllUrl()
    for url in urls:
        print('当前网址=>', url)
        text = getDetailPage(url)
        parseDetailPage(text)
