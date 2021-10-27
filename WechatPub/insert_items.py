# encoding: utf-8
"""
@project = Py_learing
@file = insert_items
@author= wanghu
@create_time = 2021/8/25 10:46
"""
import time

from WechatPub.CONFIG import *
import pymysql
import logging
logging.basicConfig(level=logging.INFO)

class Items():
    def __init__(self):
        self.conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DATABASE, charset=DB_CHARSET)
        self.cur = self.conn.cursor()

    def insertItem(self, item):
        title = self.addslashes(item['title'])
        author = item['author']
        pubitme = item['pubtime']
        content = item['abstract']
        url = item['url']
        info = self.addslashes(item['info'])
        sql = '''INSERT INTO `WechatPub` (title, author, pubtime, content, url, info, add_time) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", %s)''' % (title, author, pubitme, content, url, info, int(time.time()))
        self.cur.execute(sql)
        self.conn.commit()
        logging.info('插入成功！')

    def commit_db(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def close(self):
        self.cur.close()
        self.conn.close()

    def addslashes(self, s):
        l = ["\\", '"', "'", "\0", ]
        for i in l:
            if i in s:
                s = s.replace(i, '\\' + i)
        return s