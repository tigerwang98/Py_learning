# encoding: utf-8
"""
@project = Py_learing
@file = test13
@author= wanghu
@create_time = 2021/12/24 14:25
"""
import re
from dateparser import parse
from selenium import webdriver
import time
from lxml import etree
from selenium.webdriver.chrome.options import Options
import requests
import pymysql
from url_test.test_upload_file import processFile

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}
# conn_252 = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='test')
conn_252 = pymysql.connect(host='192.168.1.252', user='wanghu', password='wanghu123', port=3306, db='suidaobig')
cursor_252 = conn_252.cursor()
conn_241 = pymysql.connect(host='192.168.1.241', user='wanghu', password='wanghu123', port=3306, db='onlyForCrawler')
cursor_241 = conn_241.cursor()

def addslashes(s):
    l = ["\\", '"', "'", "\0", ]
    for i in l:
        if i in s:
            s = s.replace(i, '\\' + i)
    return s

def insert_bidnew(items):
    info = addslashes(items[7]) if items[7] else items[7]
    sql_252 = '''INSERT INTO `stang_bid_new`(area_id, cate_id, title, author, pubtime, outurl, location, info, add_time) VALUES(%s, %s, "%s", "%s", "%s", "%s", "%s", "%s", %s)''' % \
          (items[0], items[1], items[2], items[3], items[4], items[5], items[6], info, int(time.time()))
    cursor_252.execute(sql_252)
    insert_id = cursor_252.lastrowid
    conn_252.commit()
    return insert_id


def insert_gofast(file_list, insert_id, table_name='stang_bid_new'):
    for file in file_list:
        file_url, file_name = file.get('file_url'), file.get('file_name')
        intro = processFile(file_url, file_name)
        if not intro:
            continue
        print('文件上传成功！')
        print('文件本地服务器地址为：%s' % intro)
        sql_241 = 'insert into go_fastdfs_file_url(table_id, fileurl, `table_name`) values (%d, "%s", "%s")' % (
        insert_id, intro, table_name)
        cursor_241.execute(sql_241)
        conn_241.commit()

if __name__ == '__main__':
    item = []
    data_id = insert_bidnew(item)
    insert_gofast(item[-1], data_id, table_name='stang_bid_new')
