# encoding: utf-8
"""
@project = scrapy_zixun
@file = start_scrapy
@author= wanghu
@create_time = 2021/9/24 15:41
"""
from scrapy import cmdline
from redis import Redis

if __name__ == '__main__':
    redis_conn = Redis(host='localhost', port=6379, db='7', password='')
    print('初始url已设置！')
    start_url = 'http://fzggw.cq.gov.cn/'
    redis_conn.lpush('Chongqing_fgw', start_url)
    cmdline.execute(['scrapy', 'crawl', 'Chongqing_fgw'])