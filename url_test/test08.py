# encoding: utf-8
"""
@project = temp
@file = test08
@author= wanghu
@create_time = 2021/7/19 10:50
"""
import time
import requests
from selenium import webdriver

url = r'https://www.eco-city.gov.cn/html/zbgg/index_2.html'
'''header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    # 'Cookie': 'Hm_lvt_204fe1c74cbe57b1a3027197a128b614=1626228138,1626662960; zX2lkc3RdSTATUS=0000000350df72e602da305626bbf4d2b09e7c5a3816183a5c7e90b2d4f6; VudF9fX19lEVENT=ely7gKjbsMSHQQHv; Hm_lpvt_204fe1c74cbe57b1a3027197a128b614=1626663214',
}
param = {

}

resp = requests.get(url=url, headers=header)
print(resp.status_code)
print(resp.text)'''
path = r'../chromedriver_win32/chromedriver.exe'
with open(r'CA030440000404041530003.js', 'r', encoding='utf-8') as f:
    script_str = f.read()

driver = webdriver.Chrome(executable_path=path)
driver.get(url)
time.sleep(5)
cookie = driver.execute_script(script=script_str)
print(cookie)
driver.close()
driver.quit()