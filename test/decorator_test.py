# encoding: utf-8
"""
@project = Py_learning
@file = decorator_test
@author= wanghu
@create_time = 2021/7/29 15:15
"""
'''
闭包： 就是函数，但是与普通函数的区别是可以访问“外部”的变量，以完成封装的功能 如：
def A(name):
    def B():
        print(name)     # 这里使用了A里面的name
        return B()
-----------------------------------------------------------------------------------


'''
import time

def B(level):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            if level == 'DEBUG':
                return func(*args, **kwargs)
            elif level == 'INFO':
                print('当前时间:', int(time.time() * 1000), '进入了函数:', func.__name__, sep=' ',)
                print('你好！年龄是%s的%s' % (kwargs['age'], kwargs['name']))
                return func(*args, **kwargs)
        return inner_wrapper
    return wrapper

@B(level='INFO')
def A(name, age):
    print('Hello! %s' % name)

@B(level='DEBUG')
def C(name, age):
    print('Hello! %s' % name)

if __name__ == '__main__':
    A(name='Bob', age=18)
    C(name='Lily', age=20)