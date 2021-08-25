# encoding: utf-8
"""
@project = Py_learing
@file = CONFIG
@author= wanghu
@create_time = 2021/8/18 16:57
"""
# 要抓取的公众号列表
URL_CONFIG = './authors.txt'
# 爬虫的headers
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
}
# 当前列表页与详情页是跨域情况，请注释第一行
# BASE_URL = ''
LIST_BASE_URL = 'https://weixin.sogou.com/weixin?'
DETAIL_BASE_URL = 'https://weixin.sogou.com'
# 要抓取的页数
PAGE = 10
