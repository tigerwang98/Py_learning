# encoding: utf-8
"""
@project = Py_learing
@file = 001
@author= wanghu
@create_time = 2021/9/9 10:38
"""
import threading
import time

def method_t1(thread_name, test_param, name, age):
    while True:
        print('This is thread %s!'% thread_name)
        print('hello', name, end=' ')
        print('age:', age)
        print(test_param)
        time.sleep(1)

def method_t2(thread_name, test_param, name, age):
    while True:
        print('This is thread %s!'% thread_name)
        print('hello', name, end=' ')
        print('age:', age)
        print(test_param)
        time.sleep(1)

t1 = threading.Thread(target=method_t1, args=('t1', 'haha'), kwargs={'name': 'xiaoming', 'age': 18})
t2 = threading.Thread(target=method_t2, args=('t2', 'xixi'), kwargs={'name': 'Lily', 'age': 20})

t1.start()
t2.start()
print('*******************************')
t1.join()
t2.join()