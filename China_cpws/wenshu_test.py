# coding = utf-8
import re
import time
import random
import requests
import datetime
import json
import base64
from Crypto.Cipher import DES3
from wenshu_des import Des

def get_sessionid():
    pass

def get_pageId():
    header = {
    }
    url = "https://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html?"

    res = requests.get(url)
    if res.status_code == 200:
        print(res.text)
    else:
        print(res.status_code)

def productor():
    url = "https://wenshu.court.gov.cn/website/parse/rest.q4w"
    cipher = make_ciphertext()
    header = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "SESSION=1fde4d39-e1ad-4ade-b067-00ce88c44ac1",
        "Host": "wenshu.court.gov.cn",
        "Origin": "https://wenshu.court.gov.cn",
        "Referer": "https://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    param = {
        # "pageId": "b85247396aea1d4b30617faa58edec54",
        "s21": "中建二局",
        "sortFields": "s50:desc",
        "ciphertext": cipher,
        "pageNum": "1",
        "queryCondition": '[{"key":"s21","value":"中建二局"}]',
        "cfg": "com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@queryDoc",
        "__RequestVerificationToken": make_requestvertificationtoken(),
    }
    res = requests.post(url=url, headers=header, data=param).json()
    if res['code'] == 1:
        data = res['result']
        secretkey = res['secretKey']
        text = decrypt_result(data, secretkey)
        # print(text)
        data = text_handle(text)
        return data
    else:
        print(res)

def text_handle(text):
    title_pattern = r""""1":"[\s\S\u4e00-\u9fa5]+?","""
    fayuan_pattern = r""""2":".*?",?"""
    cply_pattern = r""""26":"[\s\S\u4e00-\u9fa5]+?","""
    rk_pattern = r""""rowkey":".*?",?"""
    pubtime_pattern = r""""31":".*?",?"""

    ptitle = re.compile(title_pattern)
    pfayuan = re.compile(fayuan_pattern)
    pcply = re.compile(cply_pattern)
    prk = re.compile(rk_pattern)
    ppubtime = re.compile(pubtime_pattern)

    titles = ptitle.findall(text)
    fayuans = pfayuan.findall(text)
    cplys = pcply.findall(text)
    rks = prk.findall(text)
    pubtimes = ppubtime.findall(text)
    result = []
    for index in range(5):
        title = titles[index].split(':')[-1].strip(',').strip("'").strip(' ').lstrip("'").strip('"')
        fayuan = fayuans[index].split(':')[-1].strip(',').strip("'").strip(' ').lstrip("'").strip('"')
        cply = cplys[index].split(':')[-1].strip(',').strip("'").strip(' ').lstrip("'").strip('"')
        rk = rks[index].split(':')[-1].strip(',').strip("'").strip(' ').lstrip("'").strip('"')
        pubtime = pubtimes[index].split(':')[-1].strip(',').strip("'").strip(' ').lstrip("'").strip('"')
        result.append({
            'title': title,
            'fayuan': fayuan,
            'cply': cply,
            'rk': rk,
            'pubtime': pubtime,
        })
    return result

def make_requestvertificationtoken():
    str = ""
    arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
           'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
    for i in range(24):
        str += arr[round(random.random() * (len(arr)-1))]
    return str

def make_ciphertext():
    timestamp = str(int(time.time() * 1000))
    salt = ''.join([random.choice('0123456789qwertyuiopasdfghjklzxcvbnm') for _ in range(24)])
    iv = datetime.datetime.now().strftime('%Y%m%d')
    des = Des()
    enc = des.encrypt(timestamp, salt)
    strs = salt + iv + enc
    result = []
    for i in strs:
        result.append(bin(ord(i))[2:])
        result.append(' ')
    return ''.join(result[:-1])

def decrypt_result(text, key):
    iv = datetime.datetime.now().strftime('%Y%m%d').encode()
    cryptor = DES3.new(key, DES3.MODE_CBC, iv)
    de_text = base64.standard_b64decode(text)
    plain_text = cryptor.decrypt(de_text)
    out = unpad(plain_text.decode('utf-8'))
    return out

def unpad(s):
    return s[0:-ord(s[-1])]

def consumer(data):
    result = []
    for item in data:
        url = "https://wenshu.court.gov.cn/website/parse/rest.q4w"
        header = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "SESSION=1fde4d39-e1ad-4ade-b067-00ce88c44ac1",
            "Host": "wenshu.court.gov.cn",
            "Origin": "https://wenshu.court.gov.cn",
            "Referer": "https://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html?docId=%s"%item['rk'],
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        param = {
            'docId': item['rk'],
            'ciphertext': make_ciphertext(),
            'cfg': 'com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@docInfoSearch',
            '__RequestVerificationToken': make_requestvertificationtoken()
        }
        res = requests.post(url=url, headers=header, data=param).json()
        if res['code'] == 1:
            text = res['result']
            secretkey = res['secretKey']
            data = json.loads(decrypt_result(text, secretkey))
            print(data)
            anjian_leixing = data['s8']
            anjian_jieduan = data['s9']
            xuanpan_time = data['s31']
            pubtime = data['s41']
            panjueshu_id = data['s22']
            jianjie = data['s23']
            # shangsuliyou = data['s25']
            benyuanrenwei = data['s26']
            jieguo = data['s27']
            shenpan_people = data['s28']
            detail = data['qwContent']
            time.sleep(2)
        else:
            print(res)

if __name__ == "__main__":
    productor_data = productor()
    consumer(productor_data)
