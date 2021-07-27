import json

import pymysql
from redis import Redis

def connect_db():
    db = pymysql.connect(host='192.168.1.252', user='wanghu', password='wanghu123',db='company')
    rds = Redis(host='192.168.1.196', password='', db=0, port=6379)
    cursor = db.cursor()
    return cursor,rds

def select(cursor, companyName="中铁十八局集团有限公司"):
    sql = 'SELECT cid FROM stang_company_kaiting WHERE companyName="{}" LIMIT 1'.format(companyName)
    cursor.execute(sql)
    result = cursor.fetchone()
    return result[0]

def push_redis(rds, companyName, cid):
    rds.lpush('kt_company_queue',
                    json.dumps(
                        {"company_name": companyName, "company_id": cid, "pid": company_pid, "tags": []}))

if __name__ == "__main__":
    cursor, rds = connect_db()
    cid = select(cursor)
