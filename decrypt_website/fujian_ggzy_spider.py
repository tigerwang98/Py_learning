import json
import requests
import time
import math

url = 'https://ggzyfw.fujian.gov.cn/Trade/TradeInfo'
header = {
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}
param = '''{"AREACODE":"","M_PROJECT_TYPE":"","KIND":"GCJS","GGTYPE":"1","PROTYPE":"","timeType":"6","BeginTime":"2020-09-19 00:00:00","EndTime":"2021-03-19 23:59:59","createTime":[],"pageNo":1,"pageSize":10,"total":8892,"ts":1616146536887}'''#%math.ceil(time.time()*1000)
print(param)
res = requests.post(url=url, headers=header, data=json.dumps(param))
res.encoding = 'utf-8'
print(res.text)