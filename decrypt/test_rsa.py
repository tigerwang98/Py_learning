# encoding: utf-8
"""
@project = temp
@file = test_rsa
@author= wanghu
@create_time = 2021/6/29 17:01
"""
import rsa
import base64
import requests
import execjs

def get_passwd():
    with open(r'jsencrypt.min.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
    ctx = execjs.compile(js_code)
    passwd = ctx.call('get_pswd', '888888')
    # print(passwd)
    return passwd

def send_url(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'X-Xsrftoken': 'GO2VD1c0LXFAPSCmjJ6tg8sxeFVBM5vw',
        'Cookie': 'zhiliao_website=a18d81b49e56183d6cc7372b46c680fd; _xsrf=R08yVkQxYzBMWEZBUFNDbWpKNnRnOHN4ZUZWQk01dnc=|1626426372310031258|9da3a4056e3be4ec240c108f07f2828e3648d356f7f2f81050dab446a59cb124',
    }
    param = {
        'uid': '18899990000',
        'password': get_passwd(),
    }
    resp = requests.post(url=url, headers=header, data=param)
    print(resp.text)


request_url = 'https://www.zlkt.net/training/jscrack/project/1/login.api?CourseId=1&BarId=13'
send_url(request_url)