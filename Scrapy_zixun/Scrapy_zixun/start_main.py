# encoding: utf-8
"""
@project = Scrapy_zixun
@file = start_main
@author= wanghu
@create_time = 2021/9/26 15:03
"""
from scrapy import cmdline
from redis import Redis


spider_name = 'Chongqing_caizheng'

if __name__ == '__main__':
    redis_key = 'Chongqing_caizheng_start'
    start_url = 'http://czj.cq.gov.cn/'
    redis_conn = Redis(host='localhost', password='', db='7', port=6379)
    cmd_array = ['scrapy', 'crawl', 'Chongqing_caizheng']
    redis_conn.lpush(redis_key, start_url)
    cmdline.execute(cmd_array)

