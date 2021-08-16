# encoding: utf-8
"""
@project = Py_learing
@file = test11
@author= wanghu
@create_time = 2021/8/16 16:05
"""
import requests
import json

url = 'http://192.168.1.112:8000/d4ocr/'
pic_path = r'C:\\Users\\123\\Desktop\\test.jpg'
with open(pic_path, 'rb') as f:
    file = f.read()

files = {'doocr': file}

res = requests.post(url=url, files=files)
print(res.text)
print(res.status_code)