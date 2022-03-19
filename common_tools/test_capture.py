from common_tools.handle_recapture import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from lxml import etree
from selenium.webdriver.chrome.options import Options

username = '17792209843'

webdriver_path = r'C:\\Users\\Administrator\\Desktop\\Py_learning\\chromedriver_win32\\chromedriver.exe'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
}
bg_img_path = r'bg_img.png'
slide_img_path = r'slide_img.png'
url = 'https://www.zhihu.com/signin?next=%2F'

def get_png(page_source):
    html = etree.HTML(page_source)
    bg_img = html.xpath('//div[@class="yidun_bgimg"]//img[@class="yidun_bg-img"]/@src')[0]
    slide_img = html.xpath('//div[@class="yidun_bgimg"]//img[@class="yidun_jigsaw"]/@src')[0]
    with open(bg_img_path, 'wb') as f:
        res = requests.get(bg_img, headers=header)
        if res.status_code == 200:
            f.write(res.content)
    with open(slide_img_path, 'wb') as f:
        res = requests.get(slide_img, headers=header)
        if res.status_code == 200:
            f.write(res.content)

def get_driver_obj(chrome_driverPath, save_path):
    chrome_opt = Options()
    chrome_opt.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    )
    chrome_opt.add_argument(
        '--disable-blink-features=AutomationControlled'
    )
    driver = webdriver.Chrome(executable_path=chrome_driverPath, options=chrome_opt)
    with open(save_path[0], 'r', encoding='utf-8') as f:
        js = f.read()
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })
    return driver

if __name__ == '__main__':
    js_path = r'C:\\Users\\Administrator\\Desktop\\Py_learning\\test\\douyin_selenium\\hidden_js\\stealth.min.js',
    driver = get_driver_obj(webdriver_path, js_path)
    driver.get(url)
    driver.find_element(By.XPATH, '//input[@name="username"]').send_keys(username)
    time.sleep(1)
    driver.find_element(By.XPATH, '//button[@class="Button CountingDownButton SignFlow-smsInputButton Button--plain"]').click()
    time.sleep(10)
    get_png(driver.page_source)
    tracks = get_validate_param(bg_img_path, slide_img_path)
    slider = driver.find_element(By.XPATH, '//div[@class="yidun_slider"]')
    # move_to_gap(driver, slider, tracks)
    s = get_validate_param(bg_img_path, slide_img_path)
    t = generate_tracks(s)
    move_to_gap(driver, slider, t)
    time.sleep(1000)


    driver.quit()