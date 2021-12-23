import re
import sys
import time
from dateparser import parse
import aiohttp
import asyncio
import logging
import elasticsearch

logging.basicConfig(level=logging.INFO)
logger = logging
index_name = 'bookstore'
index_type = 'book'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
}
es = elasticsearch.Elasticsearch()
pg = 1

def create_index():
    logger.info('正在创建索引... ...')
    es.indices.create(index=index_name, ignore=400)
    logger.info('索引创建成功!')

def get_standard_pubtime(pub_time):
    if not isinstance(pub_time, str):
        try:
            pub_time = str(pub_time)
        except Exception as e:
            print(e)
            raise TypeError
    if pub_time.strip() == '-':
        return '-'
    pub_time = re.sub(r'\\r|\\n|\\t', '', pub_time)
    pubtime = parse(pub_time)
    if pubtime:
        return str(pubtime).split(' ')[0]
    else:
        # logger.info('%s 时间格式不对！' % pub_time)
        pubtime = '————'
        return pubtime

def insert_data(datas):
    for data in datas:
        result = es.index(index=index_name, document=data)
        logger.info('%s插入成功!' % data['book_name'])

async def request_book(page):
    logger.info('正在爬取第%s页' % page)
    url = 'https://spa5.scrape.center/api/book/?limit=18&offset=%s' % ((page - 1) * 18)
    res = await do_request(url)
    datas = await parse_detail(res, page)
    for data in datas:
        print(data['book_id'], data['book_name'], data['outurl'])
    insert_data(datas)

async def parse_detail(res, page):
    logger.info('开始解析第%s页的数据' % page)
    datas = []
    for item in res['results']:
        bid = item['id']
        name = item['name']
        author = ",".join(item['authors']).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        cover = item['cover']
        score = item['score']
        logger.info('%s开始解析... ...' % name)
        url = 'https://spa5.scrape.center/api/book/' + bid
        ret = await do_request(url)
        introduction = ret['introduction']
        isbn = ret['isbn']
        page_number = ret['page_number']
        price = ret['price']
        publisher = ret['publisher']
        pubtime = get_standard_pubtime(ret['published_at'])
        tags = ret['tags']
        comments = ret['comments']
        href = ret['url']
        catelog = ret['catalog']
        data = {
            'book_id': bid, 'book_name': name, 'book_author': author, 'book_cover': cover, 'book_score': score,
            'book_isbn': isbn, 'book_page': page_number, 'price': price, 'publisher': publisher,
            'pubtime': pubtime, 'book_tags': tags, 'comments': comments, 'detail_url': url, 'outurl': href,
            'introduction': introduction, 'catelog': catelog
        }
        if pubtime == '————':
            print('catch:', name)
        datas.append(data)
    return datas

async def do_request(url):
    # connector = aiohttp.TCPConnector(limit=50)
    timeout = aiohttp.ClientTimeout(total=100)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, headers=header) as response:
            if response.status == 200:
                return await response.json()
'''
错误代码
async def do_request(url):
    session = aiohttp.ClientSession()
    async with session.get(url, headers=header) as response:
        await session.close()
        print(response.json())
        print(await response.json())
        return await response.json()
'''

if __name__ == '__main__':
    logger.info('start_time: %s' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    # create_index()
    loop = asyncio.get_event_loop()
    # 开启10个协程
    tasks = []
    while pg < 50:
        for i in range(10):
            task = asyncio.ensure_future(request_book(pg))
            pg += 1
            tasks.append(task)
        loop.run_until_complete(asyncio.wait(tasks))
    logger.info('end_time: %s' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

# ------------------------------------------------------------------------
    #   async with aiohttp.ClientSession() as session:
    #     async with session.get(url, params=param) as response:
    #         print(await response.text())