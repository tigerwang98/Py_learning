# encoding: utf-8
"""
@project = Scrapy_fagui
@file = start
@author= wanghu
@create_time = 2022/1/10 11:48
"""
from scrapy.cmdline import execute
cmd_array = ['scrapy', 'crawl', 'Sichuan_ggzy']

execute(argv=cmd_array)