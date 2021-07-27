# encoding: utf-8
"""
@project = temp
@file = test_chrome
@author= wanghu
@create_time = 2021/6/24 11:02
"""
from lxml import etree
import requests
import time
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
import random
import logging
logging.basicConfig(level=logging.INFO)


changed_company = []
company = []
chrome_path = './chromedriver.exe'
url = 'http://192.168.1.241:5920/api/task?page_size=20&page=1&id=&protocol=&name=&tag=&host_id=&status='

option = ChromeOptions()
option.add_argument('--headless')
driver = Chrome(executable_path=chrome_path)

def company_list():
    logging.info('正在查询数据库产生公司列表...')
    company_txt = '''
    伟拓招标采购交易平台
    大华集团
    漯河市公共资源交易信息网'''
    for com in company_txt.split('\n'):
        company.append(com.strip())

def login():
    logging.info('正在登录...')
    url = 'http://192.168.1.241:5920/'
    driver.get(url)
    account = driver.find_element_by_xpath('//input[@type="text"]')
    psword = driver.find_element_by_xpath('//input[@type="password"]')
    login_btn = driver.find_element_by_xpath('//button[@class="el-button el-button--primary"]')
    account.send_keys('Daddy')
    psword.send_keys('admin123')
    login_btn.click()

def edit_cron(company_name):
    time.sleep(1)
    edit_button_list = driver.find_elements_by_xpath('//tbody//tr')
    if len(edit_button_list) < 1:
        return False
    edit_button_list[0].find_element_by_xpath('.//button[@class="el-button el-button--primary"]').click()
    crontab_input = driver.find_element_by_xpath('//div[@class="el-input"]/input[@placeholder="秒 分 时 天 月 周"]')
    time.sleep(1)
    # 清除当前框中的内容
    crontab_input.send_keys(Keys.CONTROL, 'a')
    time.sleep(1)
    cron_expres = '%s %s 6-22 * * *' % (random.randint(1, 60), random.randint(1, 60))
    logging.info('更改后的定时任务表达式是：%s' % cron_expres)
    crontab_input.send_keys(cron_expres)
    time.sleep(1)
    ok_btn = driver.find_element_by_xpath('//button[@class="el-button el-button--primary"]')
    ok_btn.click()
    return True

def find_edit_btn(company_name):
    status = edit_cron(company_name)
    if status:
        changed_company.append(company_name)
        logging.info('%s修改成功！'%company_name)
    else:

        logging.info('%s修改失败！'%company_name)

def search(company_name):
    logging.info('当前的爬虫是:%s'%company_name)
    a = driver.find_elements_by_xpath('//form//div[@class="el-row"]')[0]
    time.sleep(2)
    b = a.find_elements_by_xpath('.//div[@class="el-form-item"]')[1]
    time.sleep(2)
    search_input = b.find_element_by_xpath('.//input[@class="el-input__inner"]')
    time.sleep(2)
    search_input.send_keys(company_name)
    search_btn = driver.find_element_by_xpath('//button[@class="el-button el-button--primary"]')
    search_btn.click()


if __name__ == '__main__':
    login()
    company_list()
    for company_name in company:
        time.sleep(1)
        search(company_name)
        find_edit_btn(company_name)

    driver.quit()
    driver.close()
    logging.info('修改过的爬虫有：')
    print(changed_company)

