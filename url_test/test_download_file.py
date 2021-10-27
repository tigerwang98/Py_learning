# encoding: utf-8
"""
@project = Py_learing
@file = test11
@author= wanghu
@create_time = 2021/10/8 9:41
"""
import requests

url = 'http://zjpubservice.zjzwfw.gov.cn/zhejiang/7cefe60e-fbff-45ef-9f8e-4dd920a36568/fded2b9a-afb4-425b-b66d-e8d794f3f9a2/%E5%BA%84%E5%B8%82%E8%A1%97%E9%81%93%E5%9F%8E%E5%B8%82%E5%93%81%E8%B4%A8%E6%8F%90%E5%8D%87-%E4%B8%BB%E8%A6%81%E9%81%93%E8%B7%AF%E6%B2%BF%E7%BA%BF%E5%A4%9C%E6%99%AF%E7%85%A7%E6%98%8E%E6%8F%90%E5%8D%87%E5%B7%A5%E7%A8%8B%E8%AE%BE%E8%AE%A1%E9%87%87%E8%B4%AD%E6%96%BD%E5%B7%A5%EF%BC%88EPC%EF%BC%89%E6%80%BB%E6%89%BF%E5%8C%85.pdf'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}
res = requests.get(url, headers=header)
with open(r'xxx.pdf', 'ab+') as f:
    f.write(res.content)