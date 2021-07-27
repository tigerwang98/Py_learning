# encoding: utf-8
"""
@project = temp
@file = youdao_translate
@author= wanghu
@create_time = 2021/7/26 10:09
"""
import json
import requests
import hashlib
import time
import random
from urllib.parse import urlencode

input_str = input('请输入要翻译的文字：').encode()
appVersion = '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
ts = int(time.time()*1000)
salt = str(ts) + str(int(10 * random.random()))
bv_obj = hashlib.md5()
bv_obj.update(appVersion.encode('utf-8'))
bv = bv_obj.hexdigest()
sign_obj = hashlib.md5()
sign_obj.update(b'fanyideskweb' + input_str + salt.encode() + b'Y2FYu%TNSbMCxc3t2u^XT')
sign = sign_obj.hexdigest()

def send_post():
    url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'STUDY_SESS="j9PL02AiNAqNoWbCfAn0exci6H21ky3MPhYTDx7GCZcRYIq1hpPubvXXF2+o5W6Zc6aJZj1elvzsMUfUppFicolIwSGABfa23m3h3M/X1o+7sjAAzKMMjGUkGIB03bjF22UQtHi/AIhS7UXxu0YpUCmkyOsT6RkaoWRuF0ku8ugvhQFx7kzH+3GA01euhE5D"; STUDY_INFO="lyfshiwoer@163.com|-1|1022351181|1627263627205"; DICT_SESS=v2|tixRZ8uyQBPukLUfhMlf0g4nMkfPLkfR6Fn4TzhLzGRq46Mkf6MkGROA6MTBk4T4RlM64pBkMUE0pFnM6BnLlW0Q4nMzAh4g40; DICT_LOGIN=1||1627263627414; OUTFOX_SEARCH_USER_ID=1650786640@10.169.0.102; JSESSIONID=aaaLrrdeNq-8A_d6iIGRx; OUTFOX_SEARCH_USER_ID_NCOO=1591118077.8534594; ___rl__test__cookies=1627264718835',
        'Referer': 'https://fanyi.youdao.com/',
    }
    param = {
        'i': input_str.decode(),
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salt,
        'sign': sign,
        'its': ts,
        'bv': bv,
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME',
    }
    ret = requests.post(url=url, headers=header, data=param)
    print(ret.text)

send_post()