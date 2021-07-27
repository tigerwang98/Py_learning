# _*_ coding:utf-8 _*_
from pprint import pprint
import logging, sys, json, time, random
import requests
import redis
import pymysql
from requests.packages import urllib3
from decorator import checkConnect

urllib3.disable_warnings()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s-[%(threadName)s] : %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class PID:
    def __init__(self):
        self.redis = redis.StrictRedis(connection_pool=redis.ConnectionPool(host='192.168.1.196', port=6379, decode_responses=True))
        self.conn = pymysql.connect(host='192.168.1.252', user='root', passwd='123asd123asd', db='suitang')
        self.cursor = self.conn.cursor()
        self.proxy = self.get_proxy_ip()
        self.key_list = ['kt_company_queue']
        self.filter = []

    def get_proxy_ip(self):
        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": "u5694.5.tp.16yun.cn",
            "port": "6445",
            "user": "16RNXKFD",
            "pass": "604155",
        }
        # 设置 http和https访问都是用HTTP代理
        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        return proxies
    
    def delete(self):
        for key in self.key_list:
            self.redis.delete(key)
            logging.info(f'{key} 删除成功!')
    
    def get_data(self, company):
        url = 'https://aiqicha.baidu.com/smart/searchListAjax'
        params = {
            'q': company,
            't': 0,
            'p': 1,
            's': 10,
            'o': 0,
            'f': 'null'
        }
        headers = {
            'Host': 'aiqicha.baidu.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'content-type': 'application/json',
        }
        retry_nums, res = 4, None
        while retry_nums >= 0:
            try:
                response = requests.get(url, params=params, proxies=self.proxy, headers=headers, verify=False)
                if response.status_code == 200:
                    res = response.json()
                    break
                else:
                    retry_nums -= 1
                    logging.info(f'请求【{company}】数据失败!当前状态码为: {res.status_code} 正在进行{4 - retry_nums}次重试!')
            except Exception as e:
                time.sleep(1.5)
                retry_nums -= 1
                logging.info(f'请求【{company}】数据出错!原因为: {str(e)} 正在进行第{4 - retry_nums}次重试!')
        return res

    def get_pid(self, data: dict, company):
        pid, tags = -1, []
        if not data:
            return pid, tags
        try:
            infos = data['data']['resultList']
            for info in infos:
                if company == info.get('titleName'):
                    pid, tags = info.get('pid', -1), info.get('tags', [])
        except Exception as e:
            logging.info(f'处理公司列表数据失败! 原因为: {str(e)}')
        return pid, tags

    def __conn_252(self):
        try:
            conn = pymysql.connect(host='192.168.1.252', user='root', passwd='123asd123asd', db='suitang')
            return conn
        except Exception as e:
            logging.info(f'连接数据失败!原因为: {str(e)}')
            return None

    @checkConnect
    def gen_company(self, fail_nums=3):
        if self.redis.llen('enterprise_company_id') > 0:
            return
        while True:
            intelligence_list = self.__get_intelligence_list()
            if (not intelligence_list) or fail_nums <= 0:
                logging.info(f'资质列表长度为{len(intelligence_list)} AND 失败次数为{3 - fail_nums} 退出生产!')
                break
            intelligence = intelligence_list.pop()
            sql = 'SELECT DISTINCT(forid) FROM stang_company_intelligence WHERE intelligence="{}"'.format(intelligence)
            try:
                self.cursor.execute(sql)
                for company_id in [res[0] for res in self.cursor.fetchall() if res[0] not in self.filter]:
                    self.filter.append(company_id)
                    data = json.dumps({'intelligence': intelligence, 'company_id': company_id})
                    self.redis.lpush('enterprise_company_id', data)
                logging.info(f'【{intelligence}】公司id生产完毕!剩余{len(intelligence_list)}个资质未生产~~~')
            except Exception as e:
                logging.info(f'获取【{intelligence}】公司列表id失败!原因为: {str(e)}')
                intelligence_list.append(intelligence)
                fail_nums -= 1
            with open(r'company.txt', 'w', encoding='utf-8') as txt:
                txt.write(str(intelligence_list))

    def produce(self, data):
        for key in self.key_list:
            self.redis.rpush(key, data)

    @checkConnect
    def get_company(self):
        while self.redis.llen('enterprise_company_id') > 0:
            company_info = json.loads(self.redis.rpop('enterprise_company_id'))
            company_id = company_info['company_id']
            sql = f'SELECT company_name FROM `stang_company` WHERE id={company_id}'
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            if res:
                return res[0].strip(), company_id
            logging.info(f'当前id为: {company_id} 未匹配到数据!跳过~~~')
        return 'over'

    def run(self):
        while 1:
            company, company_id = self.get_company()
            company_new = company.replace('（', '(').replace('）', ')').replace(' ', '')
            if company == 'over':
                sys.exit(0)
            data = self.get_data(company=company_new)
            if data:
                pid, tags = self.get_pid(data=data, company=company_new)
                if pid != -1:
                    q = {"company_name": company, "company_id": company_id, "pid": pid, 'tags': tags}
                    self.produce(json.dumps(q))
                    logging.info(f'【{company}】数据成功加入队列!')
                else:
                    logging.info(f'未获取到【{company}】对应的pid~~~~')

    def __get_intelligence_list(self):
        with open(r'company.txt', 'r', encoding='utf-8') as mark:
            content = eval(mark.read())
        return content


if __name__ == '__main__':
    t = PID()
    # t.delete()
    t.gen_company()
    t.run()
