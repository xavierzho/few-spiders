# 金色财经最新快讯接口
import requests
import json

header = {
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}

url = 'https://api.jinse.com/noah/v2/lives?limit=20&reading=false&source=web&flag=down&id=0'
response = requests.get(url, headers=header, timeout=5)

result = json.loads(response.text)

for item in result['list'][0]['lives']:
    timestamp = item['created_at']
    content = item['content']
    print(timestamp)
    print(content)
