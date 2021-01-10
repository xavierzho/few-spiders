"""
@Author: Jonescyna@gmail.com
@Created: 2021/1/11
"""
# 广度优先策略，优先提详情页(文章)url，完成后再请求文章链接
import asyncio
import re
import aiohttp
import aiomysql
from functools import partial
from lxml import etree
from pyquery import PyQuery as pq

headers = {
    'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/83.0.4103.116Safari/537.36'
}

base_url = "https://www.cnblogs.com/sitehome/p/{}"

seen_urls = set()
queue = asyncio.Queue()
sem = asyncio.Semaphore(value=10)  # 减少并发，防止被封ip
start_urls = [queue.put_nowait(base_url.format(i)) for i in range(200, 0, -1)]


async def fetch(url, session):
    """
    异步请求页面数据，
    :param url:请求链接
    :param session:session实例
    :return:
    """
    try:
        async with sem:  # 限制最大并发数
            async with session.get(url) as resp:
                # print(resp.url)
                # print(resp)
                seen_urls.add(resp.url)
                return await resp.text()
    except Exception as e:
        print(e)


def extract_urls(task):
    """
    提取非文章页面的url
    :param task: Future对象，获取协程返回值
    :return:
    """

    doc = etree.HTML(task.result())
    links = doc.xpath('//a/@href')
    for link in links:
        if re.match(r'^h.*cnblogs\.com/.*/p/\d+\.html$', link):
            queue.put_nowait(link)


def article_handler(pool, task):
    """
    解析文章信息，我只提取title和author字段，异步存入数据库中
    :param pool: mysql连接池
    :param task: Future对象，获取协程返回值
    :return:
    """
    doc = pq(task.result())
    title = doc('h1[class=postTitle] span').text()
    author = doc('#Header1_HeaderTitle').text()
    # print(f'{title}. The Author is {author}')
    if title:
        asyncio.create_task(save_to_mysql(pool, title))


async def save_to_mysql(pool, data):
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                insert_sql = "insert into article(title) values({})".format(data)
                await cur.execute(insert_sql)
    except Exception as e:
        print(e)


async def main():
    """
    协程入口函数
    :return:
    """
    pool = await aiomysql.create_pool(host="127.0.0.1", port=3306,
                                      user='root', password='1997',
                                      db='aiomysql_test', loop=asyncio.get_event_loop(),
                                      charset="utf8", autocommit=True
                                      )

    while not queue.empty():
        async with aiohttp.ClientSession(headers=headers) as session:
            url = await queue.get()
            if url not in seen_urls:
                task = asyncio.create_task(fetch(url, session))
                await task
                if 'html' not in url.split('.')[-1]:
                    task.add_done_callback(extract_urls)
                else:
                    task.add_done_callback(partial(article_handler, pool))


if __name__ == '__main__':
    # python 3.7+
    asyncio.run(main())
    # python < 3.7
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
