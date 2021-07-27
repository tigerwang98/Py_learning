import time
import requests
from selenium import webdriver

def test_chrome_driver(path, url):
    driver = webdriver.Chrome(executable_path=path)
    driver.get(url)
    time.sleep(5)
    print(driver.page_source)
    driver.quit()
    print('over')

def test_splash(url):
    splash_url = 'http://192.168.1.192:8050/render.html?url=%s'%url + '&wait=5'
    param = {
        'file': 'https://www.powerbeijing-ec.com/jndzzb/cgUploadController.do?openFileById%26id%3D2c9080217963812f017969968f1b1ddd',
        'amp;page': '1',
    }
    res = requests.get(url=splash_url, params=param)
    print(res.text)

if __name__ == "__main__":
    path = r'./chromedriver_win32/chromedriver.exe'
    url = 'http://ggzyjy.baiyin.gov.cn/InfoPage/demand.aspx?TenderProject=EaBm2VMDRnY%3D'
    test_chrome_driver(path, url)
    # test_splash(url)