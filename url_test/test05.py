# encoding: utf-8
"""
@project = temp
@file = test05
@author= wanghu
@create_time = 2021/6/28 16:49
"""
import requests

url = 'https://login3.scrape.center/api/login'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'ontent-Type': 'application/json;charset=UTF-8'
}
param = {
    'username': 'admin',
    'password': 'admin'
}
res = requests.post(url=url, headers=header, data=param)

param_token = res.json()['token']

h = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'Authorization': 'jwt ' + param_token
}
detail_url = r'https://login3.scrape.center/api/book/?limit=18&offset=0'
ret = requests.get(detail_url, headers=h)
print(ret.text)