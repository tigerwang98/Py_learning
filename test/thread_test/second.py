# encoding: utf-8
"""
@project = Py_learing
@file = second
@author= wanghu
@create_time = 2021/9/9 10:57
"""
import threading,pymysql
import os, time
import logging
logging.basicConfig(level=logging.INFO)

def connect_to_db():
    conn = pymysql.connect(host='localhost', user='root', password='123456', db='test')
    cursor = conn.cursor()
    logging.info('数据库连接成功！')
    return conn, cursor

def get_info_fromDB(cursor):
    sql = '''SELECT id from `wechatpub` order by id asc'''
    cursor.execute(sql)
    result = cursor.fetchall()
    logging.info('数据库查询成功！')
    return result

def run(thread_num, mutex):
    while True:
        mutex.acquire()
        with open('test.txt', 'r', encoding='utf-8') as f:
            datas = f.readlines()
            if len(datas) == 0:
                mutex.release()
                break
            data = datas[0]
            queue = datas[1:]
        os.remove('test.txt')
        with open('test.txt', 'a+', encoding='utf-8') as f:
            for line in queue:
                f.write(line)
        mutex.release()
        print('当前线程号是%s,数据id为:%s' % (thread_num, data), end='')
    logging.info('当前线程号是%s,文件为空！' % thread_num)

if __name__ == '__main__':
    logging.info('测试开始！')
    conn, cur = connect_to_db()
    ret = get_info_fromDB(cur)
    with open('test.txt', 'a+', encoding='utf-8') as f:
        for r in ret:
            f.write(str(r[0]) + '\n')
    logging.info('测试文件第一次创建成功！')

    th = []
    mutex = threading.Lock()

    for i in range(1, 3):
        th.append(threading.Thread(target=run, args=(i, mutex)))
    for t in th:
        t.start()
    time.sleep(1)
    print('here')
    for i in th:
        i.join()