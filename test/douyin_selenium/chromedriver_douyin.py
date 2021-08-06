# encoding: utf-8
"""
@project = Py_learing
@file = chromedriver_douyin
@author= wanghu
@create_time = 2021/8/6 10:20
"""
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image
import sys
import cv2

class DriverDouYin():
    def __init__(self, driver_path, start_url):
        self.chrome_driverPath = driver_path
        self.url = start_url
        self.drvier = self.get_driver_obj

    @property
    def get_driver_obj(self):
        chrome_opt = Options()
        chrome_opt.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        )
        chrome_opt.add_argument(
            '--disable-blink-features=AutomationControlled'
        )
        driver = webdriver.Chrome(executable_path=self.chrome_driverPath, options=chrome_opt)
        with open('stealth.min.js', 'r', encoding='utf-8') as f:
            js = f.read()
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })
        driver.get(url=self.url)
        return driver

    # 获取截图
    def get_img_info(self,):
        time.sleep(2)
        self.drvier.save_screenshot('./snap.png')
        web_image_obj = Image.open('./snap.png')
        img = WebDriverWait(driver=self.drvier, timeout=20,).until(EC.presence_of_all_elements_located((By.ID, 'captcha-verify-image')))
        location = img[0].location
        size = img[0].size

        top = location['y'] #255
        bottom = location['y'] + size['height'] #767
        left = location['x'] # 234
        right = location['x'] + size['width'] # 574

        return web_image_obj.crop((left, top, right, bottom))

    def get_validate_param(self, backgroundImg, validateImg):
        bg_img = cv2.imread(backgroundImg)
        tp_img = cv2.imread(validateImg)
        bg_canny = cv2.Canny(bg_img, 100, 200)
        tp_canny = cv2.Canny(tp_img, 100, 200)
        res = cv2.matchTemplate(bg_canny, tp_canny, cv2.TM_CCOEFF_NORMED)
        # 绘制方框
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        th, tw = tp_img.shape[:2]
        tl = max_loc  # 左上角点的坐标
        br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
        cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
        cv2.imwrite('./find_location.png', bg_img)  # 保存在本地

        x = max_loc[0]
        print(x)
        return x

    def move(self,):
        time.sleep(10)
        self.drvier.close()
        self.drvier.quit()
        sys.exit(1)

if __name__ == '__main__':
    spider = DriverDouYin(r'C:/Users/123/Desktop/Py_learing/chromedriver_win32/chromedriver.exe', r'https://www.douyin.com/')
    a = spider.get_img_info()
    cv2.imshow('test', a)
    cv2.waitKey(3)
    spider.move()