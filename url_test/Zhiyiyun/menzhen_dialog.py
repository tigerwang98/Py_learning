# encoding: utf-8
"""
@project = Py_learing
@file = menzhen_dialog
@author= wanghu
@create_time = 2021/11/2 13:07
"""
import os

import requests
import time

def get_file_url(search_date):
    timedelta = int(time.time() * 1000)
    url = 'http://report.zhiyijiankang.com:5396/reportExportExcel/exportOutpatientLogInfo?clinicId=8a990d915cc0b3f4015d2b57a0dd04d1&searchDate=%s&searchDateEnd=%s&commodityName=&patientName=&length=35&flag=ajax&unique=%s' \
    % (search_date, search_date, timedelta)
    header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; LIO-AN00 Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 agentweb/4.0.2  UCBrowser/11.6.4.950',
    }
    res = requests.get(url, headers=header)
    return res.json()['url']


def download_file(url, search_date):
    header = {
        'User-Agent': 'okhttp/4.0.1',
    }
    res = requests.get(url, headers=header)
    path = r'C:\Users\123\Desktop\系统导出日志\%s日志.xls' % search_date
    with open(path, 'ab+') as f:
        f.write(res.content)

if __name__ == '__main__':
    # for i in range(1, 32):
    #     if i < 10:
    #         i = '0' + str(i)
    #     search_date = '2021-10-%s' % i
        search_date = '2021-11-01'
        url = get_file_url(search_date)
        download_file(url, search_date)