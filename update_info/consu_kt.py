# encoding: utf-8
"""
@project = Py_learing
@file = consu_kt
@author= wanghu
@create_time = 2021/8/11 16:46
"""
import requests
from threading import Thread
import pymysql
import sys

# Linux下路径
# queue_file_path = ''
queue_file_path = 'C:\\new_QueueFile\\Baidu_company_fy_queue.txt'

class ConsumKtQueue():
    def __init__(self):
        self.oversize = False

    def start(self):
        Thread.__init__()


    def check_size(self, file):
        def wrapper(func):
            def inner_wrapper(*args, **kwargs):
                if sys.getsizeof(file) <= 1024 * 30:
                    self.oversize = True
                    return func(*args, **kwargs)
                else:
                    self.oversize = False
                    return func(*args, **kwargs)
            return inner_wrapper
        return wrapper

    @check_size(file=file)
    def read_to_memory(self, file_pointer):
        file_pointer.readline()


if __name__ == '__main__':
    consumer = ConsumKtQueue()
    consumer
    start()