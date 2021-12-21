import re
from dateparser import parse
import aiohttp
import asyncio
import logging
import elasticsearch
logging.basicConfig(level=logging.INFO)
logger = logging
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
}


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
        logger.info('%s 时间格式不对！' % pub_time)
        raise TypeError

def insert_data(datas):

    for data in datas:



async def request_book(page):
    logger.info('正在爬取第%s页' % page)
    url = 'https://spa5.scrape.center/api/book/?limit=18&offset=%s' % (page - 1) * 18
    res = await do_request(url)
    datas = await parse_detail(await res)
    insert_data(datas)

async def parse_detail(res):
    datas = []
    for item in res['results']:
        bid = item['id']
        name = item['name']
        author = ",".join(item['authors']).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        cover = item['cover']
        score = item['score']
        url = 'https://spa5.scrape.center/api/book/' + bid
        response = await do_request(url)
        ret = await response
        if True:
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
        datas.append(data)
    return datas

async def do_request(url):
    session = aiohttp.ClientSession()
    response = await session.get(url, headers=header)
    await session.close()
    return response.json()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    for page in range(1, 503):
        task = asyncio.ensure_future(request_book(page))
        loop.run_until_complete(task)

    #   async with aiohttp.ClientSession() as session:
    #     async with session.get(url, params=param) as response:
    #         print(await response.text())