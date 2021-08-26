# encoding: utf-8
"""
@project = Py_learing
@file = test10
@author= wanghu
@create_time = 2021/8/12 11:42
"""
from dateparser import parse
from urllib.parse import quote
print(quote('成都'))
# a中有没有b中的元素，任意一个都可以
a = ['test', 'asdsa', 'sadasd', 'dddd']
b = ['this', 'is', 'a', 'test']
final = [x for x in a if x in b]
print(final)