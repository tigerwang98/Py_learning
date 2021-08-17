# encoding: utf-8
"""
@project = Py_learing
@file = chromedriver_douyin
@author= wanghu
@create_time = 2021/8/6 10:20
"""
import logging
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
import sys,io
import cv2
from lxml import etree

logging.basicConfig(level=logging.INFO)

class DriverDouYin():
    def __init__(self, driver_path, start_url):
        self.save_path = {
            'hidden_js': 'C:\\Users\\123\\Desktop\\Py_learing\\test\\douyin_selenium\\hidden_js\\stealth.min.js',
            'bg_img_path': 'C:\\Users\\123\\Desktop\\Py_learing\\test\\douyin_selenium\\capture_imgs\\backgroudPicture.png',
            'slide_img_path': 'C:\\Users\\123\\Desktop\\Py_learing\\test\\douyin_selenium\\capture_imgs\\slidePicture.png',
        }
        self.chrome_driverPath = driver_path
        self.url = start_url
        self.drvier = self.get_driver_obj
        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        }

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
        with open(self.save_path['hidden_js'], 'r', encoding='utf-8') as f:
            js = f.read()
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })
        driver.get(url=self.url)
        return driver

    def get_img_info(self,):
        bg_img = WebDriverWait(driver=self.drvier, timeout=20,).until(EC.presence_of_all_elements_located((By.ID, 'captcha-verify-image')))
        slide_img = WebDriverWait(driver=self.drvier, timeout=20,).until(EC.presence_of_all_elements_located((By.XPATH, '//img[contains(@class, "captcha_verify_img_slide")]')))
        bg_img_url = bg_img[0].get_attribute('src')
        slide_img_url = slide_img[0].get_attribute('src')
        status = self.save_imgs(bg_img_url, slide_img_url)
        if status:
            logging.info('正在准备拖动滑块进行验证......')
            return self.save_path['bg_img_path'], self.save_path['slide_img_path']
        else:
            logging.info('写入文件失败！请检查原因！')
            return False

    # 保存验证码
    def save_imgs(self, bg_img_url, slide_img_url):
        logging.info('开始保存验证码图片......')
        bg_res = requests.get(bg_img_url, headers=self.header)
        sl_res = requests.get(slide_img_url, headers=self.header)
        if bg_res.status_code == 200 and sl_res.status_code == 200:
            with open(self.save_path['bg_img_path'], 'wb') as f:
                f.write(bg_res.content)
            logging.info('写入背景图片成功！')
            with open(self.save_path['slide_img_path'], 'wb') as f:
                f.write(sl_res.content)
            logging.info('写入滑块图片成功！')
            return True
        else:
            return False

    # 获取验证码需要移动的距离
    def get_validate_param(self, backgroundImg, validateImg):
        bg_img = cv2.imread(backgroundImg)
        tp_img = cv2.imread(validateImg)
        bg_canny = cv2.Canny(bg_img, 100, 200)
        tp_canny = cv2.Canny(tp_img, 100, 200)
        # 匹配缺口
        bg_gray = cv2.cvtColor(bg_canny, cv2.COLOR_GRAY2RGB)
        tp_gray = cv2.cvtColor(tp_canny, cv2.COLOR_GRAY2RGB)
        res = cv2.matchTemplate(bg_gray, tp_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        th, tw = tp_img.shape[:2]
        tl = max_loc  # 左上角点的坐标
        br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
        cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
        cv2.imwrite('./capture_imgs/find_location.png', bg_img)  # 保存在本地
        x = (max_loc[0] // 1.623529)
        return x

    # 进行验证码验证操作
    def drag_and_drop(self, offset):
        tracks = self.get_tracks(offset)
        knob = self.drvier.find_element_by_xpath('//div[contains(@class, "secsdk-captcha-drag-sliding")]')
        self.move_to_gap(knob, tracks)
        self.drvier.refresh()
        time.sleep(3)
        return self.drvier.page_source

    # 生成模拟鼠标轨迹
    def get_tracks(self, distance):
        tracks = []     # 移动轨迹
        current = 0     # 当前位移
        mid = int(distance * 4 / 6)      # 减速阈值
        t = 1        # 计算间隔
        v = 0        # 初速度
        while current < distance:
            if current < mid:
                a = 5       # 加速度为正2
            else:
                a = -3      # 加速度为负3
            v0 = v      # 初速度v0
            v = v0 + a * t      # 当前速度
            move = v0 * t + 1 / 2 * a * t * t       # 移动距离
            current += move     # 当前位移
            if current > distance:
                move = distance - (current - move)
            tracks.append(round(move))      # 加入轨迹
        return tracks

    # 模拟滑动滑块
    def move_to_gap(self, slider, tracks):
        # slider: 滑块对象
        action = ActionChains(self.drvier)
        action.click_and_hold(slider).perform()
        for i in tracks:
            # action会自动累加位移，除非reset这个action
            action.move_by_offset(xoffset=i, yoffset=0).perform()
            action = ActionChains(self.drvier)
        time.sleep(0.5)
        action.release().perform()

    # 彻底关闭chromedriver
    def close(self,):
        time.sleep(2)
        self.drvier.quit()
        logging.info('chromedriver 已经退出！')
        sys.exit(1)

    # 解析首页html
    def parse_index_html(self, page_source):
        html = etree.HTML(page_source)
        for li in html.xpath('//ul[@class="f3f8d90bfdc74a44ab0cbe784a4af104-scss"]//li'):
            detail_href = li.xpath('./div[1]//a[2]/@href')[0]
            title = li.xpath('./div[1]//a[2]/p//text()')[0]
            author = li.xpath('.//div[@class="d8d25680ae6956e5aa7807679ce66b7e-scss"]//a//p//text()')[0]
            pubtime = li.xpath('.//div[@class="d8d25680ae6956e5aa7807679ce66b7e-scss"]//span[@class="b32855717201aaabd3d83c162315ff0a-scss"]//text()')[0]
            print(title, author, pubtime, detail_href)

    def parse_search_html(self, page_source):
        html = etree.HTML(page_source)
        count = 0
        ul = html.xpath('//ul[@class="_3636d166d0756b63d5645bcd4b9bcac4-scss"]')[0]
        for li in ul.xpath('.//li'):
            count += 1
            url = li.xpath('.//div[@class="_863f6ea4f8ed8c3f88c51527f1ea8d43-scss"]//a[2]/@href')[0]
            title = li.xpath('.//div[@class="_863f6ea4f8ed8c3f88c51527f1ea8d43-scss"]//a[2]//p//span//text()')[0]
            author = li.xpath('.//div[@class="d8d25680ae6956e5aa7807679ce66b7e-scss"]/a/p//span//text()')[0]
            pubtime = li.xpath('.//div[@class="d8d25680ae6956e5aa7807679ce66b7e-scss"]/span//text()')[0]
            print('%s.'% count, title, author, pubtime, url)

    def keyword_search(self, keyword):
        logging.info('正在根据关键字搜索相关视频......')
        WebDriverWait(self.drvier, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@class="_28bcf0c81eecec324dc834fd9da6bc14-scss _995df5bec116ef593426dbf2a410fa26-scss"]')))[0].send_keys(keyword)
        search_button = WebDriverWait(self.drvier, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//button[@class="_913d1e3dbc906c79f2227a5d1a6e4d6c-scss"]')))[0]
        search_button.click()
        self.drvier.switch_to.window(self.drvier.window_handles[1])
        time.sleep(3)
        return self.drvier.page_source

    def scroll_curPage(self):
        logging.info('获取下一页数据中......')
        self.drvier.maximize_window()
        scroll_script = 'window.scrollBy(0, 127)'
        for i in range(4):
            print('====================================')
            print(self.drvier.page_source)
            print('====================================')
            self.drvier.execute_script(scroll_script)
            time.sleep(2)

    def start(self):
        pass

class ParsePageSource():
    def __init__(self):
        pass

    @property
    def page_source(self):
        return self.page_source

    @page_source.setter
    def page_source(self, page):
        self.page_source = etree.HTML(page)

    def start(self):
        pass

if __name__ == '__main__':
    logging.info('抖音爬虫开始！')
    spider = DriverDouYin(r'C:/Users/123/Desktop/Py_learing/chromedriver_win32/chromedriver.exe', r'https://www.douyin.com/')
    bg_img_path, slide_img_path = spider.get_img_info()
    move_distance = spider.get_validate_param(bg_img_path, slide_img_path)
    page_source = spider.drag_and_drop(move_distance)
    page = spider.keyword_search('川麻婷婷妹')
    # spider.scroll_curPage()
    spider.parse_search_html(page)
    spider.close()

