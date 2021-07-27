# encoding: utf-8
"""
@project = temp
@file = test01
@author= wanghu
@create_time = 2021/6/16 14:59
"""
import base64
import string

std_table = string.ascii_uppercase +string.ascii_lowercase + string.digits + '+/'
web_table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='

base64.b64encode(b'test')
