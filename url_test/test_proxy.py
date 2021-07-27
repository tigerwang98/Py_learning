# encoding: utf-8
"""
@project = temp
@file = test_proxy
@author= wanghu
@create_time = 2021/6/7 17:52
"""
import json

import requests

proxy_host = "u5694.20.tp.16yun.cn"
proxy_port = "6447"
proxy_user = "16NPHKSJ"
proxy_pass = "287149"


def get_proxy():
    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxy_host,
        "port": proxy_port,
        "user": proxy_user,
        "pass": proxy_pass,
    }
    proxies = {
        "https": proxyMeta
    }
    return proxies

def main():
    url = 'https://aiqicha.baidu.com/c/courtnoticedetail?pid=83819702703198&dataId=45c85e5471b74005c3e9ee170970932d'
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    }
    resp = requests.get(url=url, headers=header, proxies=get_proxy())
    # resp = requests.get(url=url, headers=header)
    if resp.status_code == 504:
        print('error')
    print(resp.status_code)
    print(resp.text)


if __name__ == '__main__':
    main()
