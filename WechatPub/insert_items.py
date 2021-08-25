# encoding: utf-8
"""
@project = Py_learing
@file = insert_items
@author= wanghu
@create_time = 2021/8/25 10:46
"""
from WechatPub.CONFIG import *
import pymysql

class Items():
    def __init__(self):
        self.conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DATABASE, charset=DB_CHARSET)
        self.cur = self.conn.cursor()

    def insertItem(self, item):
        title = item['title']
        author = item['author']
        pubitme = item['pubtime']
        content = item['abstract']
        url = item['url']
        info = item['info']
        sql = '''INSERT INTO `WechatPub` (title, author, content, url, info) VALUES ("%s", "%s", "%s", "%s", "%s", "%s")''' % (title, author, pubitme, content, url, info)
        self.cur.execute(sql)
        self.conn.commit()

    def commit_db(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def close(self):
        self.cur.close()
        self.conn.close()