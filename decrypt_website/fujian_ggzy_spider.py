import requests
import time
import hashlib
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import binascii
import base64
from lxml import etree
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

proxy_host = "u5694.20.tp.16yun.cn"
proxy_port = "6447"
proxy_user = "16NPHKSJ"
proxy_pass = "287149"

class FujianGgzySpider():
    def __init__(self):
        self.header = {
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            # 'Cookie': '__root_domain_v=.fujian.gov.cn; _qddaz=QD.949227380318117; ASP.NET_SessionId=y03opx4mcmxxvvcsochei1fm; _qdda=4-1.1; _qddab=4-pimh4h.krmvq1tl',
            # 'Referer': 'https://ggzyfw.fujian.gov.cn/web/index.html',
        }
        self.proxy = self.get_16yun()

    def get_16yun(self):
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


    def handle_list_param(self, param):
        final_str = 'BeginTime' + str(param['BeginTime']) + 'createTime' + str(param['createTime']) \
        + 'EndTime' + str(param['EndTime']) + 'GGTYPE' + str(param['GGTYPE']) + \
        'KIND' + str(param['KIND']) + 'pageNo' + str(param['pageNo']) + 'pageSize' + str(param['pageSize']) \
        + 'timeType' + str(param['timeType']) + 'total' + str(param['total']) + 'ts' + str(param['ts'])
        return final_str

    def handle_detail_param(self, param):
        final_str = 'm_id' + str(param['m_id']) + 'ts' + str(param['ts']) + 'type' + str(param['type'])
        return final_str

    def url_request(self, data):
        url = 'https://ggzyfw.fujian.gov.cn/Trade/TradeInfo'
        for page in range(1, data['page']):
            logging.info('正在抓取第%s页的数据' % page)
            param = {"AREACODE": "",
                     "M_PROJECT_TYPE": "",
                     "KIND": data['KIND'],
                    "GGTYPE": data['GGTYPE'],
                    "PROTYPE": "",
                    "timeType": "6",
                    "BeginTime": data['startime_param'],
                    "EndTime": data['curtime'],
                    "createTime": [],
                    "pageNo": page,
                    "pageSize": 10,
                    "total": 6422,
                    "ts": int(time.time() * 1000)}
            self.header['portal-sign'] = self.generate_header(param)
            res = requests.post(url=url, headers=self.header, data=json.dumps(param))
            logging.info('获取列表页成功！')
            if res.status_code == 200:
                res.encoding = 'utf-8'
                yield res.json()['Data']

    def generate_header(self, param, flag=True):
        encrypt_param = '3637CB36B2E54A72A7002978D0506CDF'
        if flag:
            p = self.handle_list_param(param)
        else:
            p = self.handle_detail_param(param)
        str_param = encrypt_param + p
        a = hashlib.md5()
        a.update(str_param.encode('utf-8'))
        return a.hexdigest()

    def decrypt(self, html_info):
        html = base64.b64decode(html_info)
        key = b'BE45D593014E4A4EB4449737660876CE'
        iv = b'A8909931867B0425'
        aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
        info = aes.decrypt(html)
        decrypt_data = unpad(info, 16).decode()
        return decrypt_data

    def parse_list(self, html):
        ls = json.loads(html)
        for item in ls['Table']:
            if item['TITLE'] == '招标公告':
                cate_id = 1
            else:
                cate_id = 2
            title = item['NAME']
            pubtime = item['TM1'].split(' ')[0]
            area = item['AREANAME']
            href = item['M_ID']
            param_type = item['M_PROJECT_TYPE']
            data = {'cate_id': cate_id, 'title': title, 'pubtime': pubtime, 'area': area, 'detail_id': href, 'param_type': param_type}
            logging.info(data)
            yield data

    def get_detail_web(self, data):
        logging.info('正在获取详情页信息......')
        url = 'https://ggzyfw.fujian.gov.cn/Trade/TradeInfoContent'
        param = {
            'm_id': str(data['detail_id']),
            'ts': int(time.time()*1000),
            'type': data['param_type'],
        }
        self.header['portal-sign'] = self.generate_header(param, flag=False)
        resp = requests.post(url=url, headers=self.header, data=json.dumps(param))
        html = self.decrypt(resp.json()['Data'])
        info = json.loads(html)['Contents']

        cate_id = data['cate_id']
        title = data['title']
        pubtime = data['pubtime']
        area = data['area']
        outurl = 'https://ggzyfw.fujian.gov.cn/web/index.html#/business/detail?cid=%s&type=GCJS'%data['detail_id']

        print(cate_id, title, pubtime, area, len(info), outurl)


    def start(self):
        logging.info('爬虫开始运行！')
        curtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        curtime_param = str(curtime).split(' ')[0] + '23:59:59'
        startime_param = str(datetime.now().year) + '-01-' + str(datetime.now().day) + ' 00:00:00'
        moudle_list = [
            {'name': '工程建设', 'curtime': curtime_param, 'startime_param': startime_param, 'KIND': 'GCJS', 'GGTYPE': '1', 'page': 5},
        ]
        for moudle in moudle_list:
            logging.info('%s模块开始！'% moudle['name'])
            encrypt_html_gen = self.url_request(moudle)
            while True:
                try:
                    encrypt_html = encrypt_html_gen.__next__()
                except StopIteration:
                    break
                logging.info('正在解密返回的数据......')
                html = self.decrypt(encrypt_html)
                logging.info('开始解析网页')
                item = self.parse_list(html)
                while True:
                    try:
                        data = item.__next__()
                        if data:
                            logging.info('正在请求详情页数据......')
                            self.get_detail_web(data)
                    except StopIteration:
                        break

if __name__ == "__main__":
    spider = FujianGgzySpider()
    spider.start()