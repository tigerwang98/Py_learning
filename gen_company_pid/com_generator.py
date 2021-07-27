from redis import Redis
import json,time,sys
import pymysql
import requests, urllib3

urllib3.disable_warnings()
def connect_to_redis():
    redis_con = Redis(host='192.168.1.196', password='', db=0, port=6379)
    return redis_con

def connect_to_sql():
    db = pymysql.connect(host='192.168.1.252', user='wanghu', password='wanghu123', db='company')
    cursor = db.cursor()
    return cursor

def get_proxy_ip():
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

def get_company_id(company_name):
    url = 'http://192.168.1.197:8013/es/getdata?companyname=' + company_name +'&page=1&size=10&correct=0'
    retry_times = 4
    while retry_times > 0:
        try:
            res = requests.get(url=url).json()
            company_id = res['data'][0]['company_id']
            return company_id
        except:
            retry_times -= 1
            time.sleep(1)
    return 1

def get_company_pid(companyname):
    url = 'https://aiqicha.baidu.com/smart/searchListAjax'
    params = {
        'q': companyname,
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
            response = requests.get(url, params=params, proxies=get_proxy_ip(), headers=headers, verify=False)
            if response.status_code == 200:
                res = response.json()
                break
            else:
                retry_nums -= 1
        except Exception as e:
            time.sleep(1)
            retry_nums -= 1
    try:
        return res['data']['resultList'][0]['pid']
    except IndexError:
        return 0

def select_cid(sql_con, companyName):
    sql = 'SELECT cid FROM stang_company_kaiting WHERE companyName="{}" LIMIT 1'.format(companyName)
    sql_con.execute(sql)
    result = sql_con.fetchone()
    if not result:
        return 0
    return result[0]

def push_data(redis_con, sql_con):
    fp = open('company.txt', 'a+', encoding='utf-8')
    with open('company_txt.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
                line = line.replace('\n', ' ')
                company_name = line[1:-2]
                company_id = get_company_id(company_name)
                if company_id == 1:
                    print("%s搜不到其cid"%line)
                    company_id = select_cid(sql_con, company_name)
                    print("查询数据库获得当前公司的cid为:%s"%company_id)
                    if company_id == 0:
                        continue
                company_pid = get_company_pid(company_name)
                if company_pid == 0:
                    print("%s爱企查搜不到！" % line)
                    fp.write('pid: ' + line)
                    continue
                print('当前向redis里插入的数据是:%s %s'%(company_name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                redis_con.lpush('kt_company_queue',
                        json.dumps({"company_name": company_name, "company_id": company_id, "pid": company_pid, "tags": []}))
        fp.close()
    print("over")
    sys.exit(-1)

def run():
    redis_conn = connect_to_redis()
    sql_con = connect_to_sql()
    push_data(redis_con=redis_conn, sql_con=sql_con)

run()







