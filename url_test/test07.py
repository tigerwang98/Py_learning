# encoding: utf-8
"""
@project = temp
@file = test07
@author= wanghu
@create_time = 2021/7/16 17:00
"""
import requests
resp = requests.get(url='http://ww1.sinaimg.cn/bmiddle/006r3PQBjw1f9xh0oubn5j30c60bndgf.jpg')


with open('001.jpg', 'wb') as f:
    f.write(resp.content)