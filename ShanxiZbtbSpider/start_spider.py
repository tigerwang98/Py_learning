# encoding: utf-8
"""
@project = temp
@file = start_spider
@author= wanghu
@create_time = 2021/7/22 11:07
"""
from scrapy import cmdline
command = ['scrapy', 'crawl', 'zhaobiao_gonggao']
cmdline.execute(command)