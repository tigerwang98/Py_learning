# encoding: utf-8
"""
@project = Py_learing
@file = yaml_test
@author= wanghu
@create_time = 2021/11/30 9:41
"""
import yaml

path = 'C:\\Users\\123\\Desktop\\config.yaml'
f = open(path, 'r', encoding='utf-8')
d = yaml.load(f)
t = d['website']
for key in t.keys():
    prize_name = t[key]['prize']
    url = t[key]['url']
    key_word = t[key]['keywords']
    apartment = key.split('(')[0].replace('(', '')
    people = t[key]['person']
    print(prize_name, key_word, people, apartment, url)
