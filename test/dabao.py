# https://cuiqingcai.com/
import requests
from redis import StrictRedis, ConnectionPool
from elasticsearch import Elasticsearch
import asyncio
import time
import aiohttp

def connect_to_redis():
    pool = ConnectionPool(host='localhost', port=6379, password='', db=0)
    r = StrictRedis(connection_pool=pool)
    r.set('name', 'Bob')
    print(r.get('name'))

def connect_to_es():
    es = Elasticsearch()
    data = {
        'title': 'test',
        'url': 'https://www.baidu.com/'
    }
    result = es.create(index='news', id=1, body=data)

    print(result)


async def execute(x):
    print('Number:', x)

def callback(task):
    print('status:', task.result())


def test_coroutine():
    start_time = time.time()
    tasks = []
    # 创建事件监听对象
    loop = asyncio.get_event_loop()
    for i in range(5):
        # 将协程对象包装成task对象
        task = asyncio.ensure_future(request_httpbin())
        tasks.append(task)
    # 将事件监听对象与task绑定并执行
    loop.run_until_complete(asyncio.wait(tasks))
    end_time = time.time()
    print('cost time:', end_time-start_time)

async def request_httpbin():
    url = 'https://www.httpbin.org/delay/5'
    # 临界区(可能导致挂起的操作，有则挂起，无则继续运行)
    res = await do_request(url)
    print('response:', res)

async def do_request(url):
    session = aiohttp.ClientSession()
    # 临界区(可能导致挂起的操作，有则挂起，无则继续运行)
    res = await session.get(url)
    # await res.text()
    await session.close()
    return res
# connect_to_es()
test_coroutine()