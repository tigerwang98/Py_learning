# encoding: utf-8
"""
@project = temp
@file = test06
@author= wanghu
@create_time = 2021/6/28 17:06
"""
import sys
sys.path.append('../../temp')
import requests
from decrypt.test_rsa import encrypt_data

header = {
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'block': 'xk1rBwumj5hjXbU9Fj2WN7Qy9S4rZH4vkwgt1xLnQEupIqLo4tKnkg/Tkyb3wKBAzmLoLkfwQcagsRPg7ybCiZNXpzUMjI/RIDkB5/BH6n/rk676fj7mAZ4xXBOp77hJjBzL8dRbHeina+mAc+RvOCU2R8PuDFREQQX9I+sSuyI=',
}
param = {
    'mail_address': "318739742@qq.com",
    # 'password': encrypt_data('Abc123456-')
    'password': 'sT8sgPLvKYh7fldPL+AR/AhU/21u1duhoBXMT6gjALxDJ5jsu8xEd9RCQkyBRPrQ2+1SR8peLNhhP20a6Yj2NN25N8bdTIwRMIVx7nLkgF2lrzKVkdpo7Yno/LjbP9UtfQBV79/O7zQTUv5T2UaMIMBfB4xRLW/nYWbDW5vxF40='
}
res = requests.post(url='https://service.fecribd.com/tfse_user/user/login', data=param).json()
print(res['info'])