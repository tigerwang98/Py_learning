# encoding: utf-8
"""
@project = temp
@file = test_signature
@author= wanghu
@create_time = 2021/7/19 9:39
"""
from selenium import webdriver

url = r'https://www.douyin.com/'
path = r'../chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(path)
driver.get(url)
with open(r'acrawler.js', 'r', encoding='utf-8') as f:
    js_str = f.read()
print(js_str)
signature = driver.execute_script(js_str)
print('=======signature==========')
print(signature)
driver.close()
driver.quit()