# encoding: utf-8
"""
@project = Py_learing
@file = test09
@author= wanghu
@create_time = 2021/8/10 16:13
"""
import requests
import json

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

proxy = get_proxy()
url = 'https://www.ronghw.cn/api/portal/websiteAnnouncement/getList/allAnnList?v=1628583286188'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
}
param = '{"page":2,"number":10,"projectCode":"","announceName":"","isBidding":[],"tenderModeId":""}'
res = requests.post(url=url, headers=header, data=param, proxies=proxy)
print(res.text)