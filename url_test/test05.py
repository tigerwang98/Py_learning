# encoding: utf-8
"""
@project = temp
@file = test05
@author= wanghu
@create_time = 2021/6/28 16:49
"""
import pymysql,time
conn = pymysql.connect(host='localhost', user='root', password='123456', database='test')
cur = conn.cursor()

item = [0, 0, '测试题目', '作者', '测试时间', '测试链接', '测试坐标', 'None']
sql = '''insert into stang_bid_new(area_id, cate_id, title, author, pubtime, outurl, location, info, add_time) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'''
sql = sql % (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], int(time.time()))

cur.execute(sql)
conn.commit()
cur.close()
conn.close()
