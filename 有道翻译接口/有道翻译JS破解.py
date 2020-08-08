# 爬虫时通过一定的规则，采集互联网数据的程序

import hashlib  # 可以计算MD5
import time
import random
import requests  # 需要安装


# 实现一个md5函数
def md5(e):
    """
    md5 信息摘要算法，可以把一串字符串加密，产生一串不可逆的字符串
    A->B not B->A
    :param e:
    :return:
    """
    e = e.encode()
    result = hashlib.md5(e)
    return result.hexdigest()  # 产生摘要


# 加密函数
def getSign(e):
    appVersion = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3941.4 Safari/537.36'
    t = md5(appVersion)
    r = f"{int(time.time() * 1000)}"  # 当前时间
    i = r + str(random.randint(0, 9))
    return {
        'ts': r,
        'bv': t,
        'salt': i,
        'sign': md5("fanyideskweb" + e + i + "n%A-rKaT5fb[Gy?;N5@Tj")
    }


# 获取响应
def youdao(e):
    url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
    data = {
        'i': 'apple',
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_CLICKBUTTION'
    }
    headers = {'Accept': 'application/json,text/javascript,*/*;q=0.01',
               'Accept-Encoding': 'gzip,deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Content-Length': '242',
               'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
               'Cookie': 'OUTFOX_SEARCH_USER_ID=-1496146827@10.169.0.84;OUTFOX_SEARCH_USER_ID_NCOO=940809535.9662846;JSESSIONID=aaaGo_LbREV4o4sZNPx6w;___rl__test__cookies=1574503264149',
               'Host': 'fanyi.youdao.com',
               'Origin': 'http://fanyi.youdao.com',
               'Referer': 'http://fanyi.youdao.com/',
               'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/79.0.3941.4Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'
               }
    sign = getSign(e)
    sign.update(data)
    response = requests.post(url, data=sign, headers=headers)

    return response.json()  # 得到json 的数据


if __name__ == '__main__':
    while True:
        word = input('请输入需要翻译的词')
        result = youdao(word)
        print(result['translateResult'])
