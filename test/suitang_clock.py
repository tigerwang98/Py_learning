# encoding: utf-8
"""
@project = Py_learing
@file = suitang_clock
@author= wanghu
@create_time = 2021/7/30 17:12
"""
import requests
import datetime, time
import random,json

today = datetime.datetime.now().strftime('%Y-%m-%d')
now_time = datetime.datetime.now().strftime('%H:%M:%S')

header = {
        'Host': 'work.cninct.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; ELS-AN00 Build/HUAWEIELS-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045409 Mobile Safari/537.36 MMWEBID/7469 MicroMessenger/8.0.7.1920(0x27001335) Process/tools WeChat/arm64 NetType/WIFI Language/zh_CN ABI/arm64',
        'content-type': 'application/json',
        'Referer': 'https://servicewechat.com/wx889445acf157a307/46/page-frame.html',
        'charset': 'utf-8',
        'Accept-Encoding': 'gzip,compress,br,deflate',
    }

def send_request(sign_time, uid):
    url = 'https://work.cninct.com/SUITANGOA?op=UploadAttendDetails&userid=%s' % uid
    print('=====================参数信息==========================')
    param = {
    "details_attend_longitude": "103.99159613715278",
    "details_attend_latitude": "30.633617621527776",
    "details_attend_date": today,
    "details_attend_time": sign_time,
    "details_attend_name": "四川省成都市武侯区武兴一路8号",
    "details_attend_reason": "",
    "login_dev": "HUAWEIELS-AN00"
    }
    print(param)
    ret = requests.post(url=url, headers=header, data=json.dumps(param))
    print('=====================打卡信息==========================')
    print(ret.text)

def login():
    url = 'https://work.cninct.com/MBORequest?op=Login'
    param = {
    "account": "18683108304",
    "password": "f379eaf3c831b04de153469d1bec345e"  # md5
}
    res = requests.post(url=url, headers=header, data=json.dumps(param))
    print('===================登录信息=========================')
    return res.json()['ext']['userid']

def genearate_random_time():
    random_s = random.randint(10, 59)
    if now_time < '09:00:00':
        random_min = random.randint(50, 59)
        sign_time = '08:%s:%s' % (random_min, random_s)
    else:
        random_min = random.randint(10, 20)
        sign_time = '18:%s:%s' % (random_min, random_s)
    return sign_time

if __name__ == '__main__':
    userid = login()
    time.sleep(1)
    sign_time = genearate_random_time()
    send_request(sign_time, userid)
