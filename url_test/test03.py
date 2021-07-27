# encoding: utf-8
"""
@project = temp
@file = test03
@author= wanghu
@create_time = 2021/6/8 10:28
"""
import requests
import time
import pytesseract
from PIL import Image

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

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
file_path = r'C:\Users\123\Desktop\validateCode.jpg'
proxy = get_proxy()

def func():
    url = 'https://cg.95306.cn/proxy/portal/elasticSearch/queryDataToEs?projBidType=01&bidType=&noticeType=&title=&inforCode=&startDate=&endDate=&pageNum=%s&projType=&professionalCode=&createPeopUnit='
    for page in range(1, 10):
        print('正在生产第%s页...'%page)
        web_url = url % page
        resp = requests.get(url=web_url, headers=header, proxies=proxy).json()
        # time.sleep(3)
        if resp['code'] == '0-0203':
            img_url = 'https://cg.95306.cn/proxy/portal/enterprise/base/loadComplexValidCodeImg?validCodeKey=%s&timestamp=%s'
            validCodeKey = int(time.time()*1000)
            image_url = img_url % (validCodeKey, validCodeKey)
            print(image_url)
            resp = requests.get(url=image_url, headers=header)
            if resp:
                print('正在储存验证码文件...')
                with open(file_path, 'wb') as f:
                    f.write(resp.content)
                    print('成功获取到验证码！')
                print('开始解析验证码')
                img = Image.open(file_path)
                validateCode = pytesseract.image_to_string(img.convert('P'))
                print('验证码是：', validateCode)
            else:
                print(resp.text)
        else:
            print(resp['data']['resultData']['result'])

if __name__ == '__main__':
    func()