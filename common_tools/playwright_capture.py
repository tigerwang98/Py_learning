import requests
from playwright.sync_api import sync_playwright
import logging
from common_tools.handle_recapture import *
from lxml import etree

logger = logging
logging.basicConfig(level=logging.INFO)

index_url = r'https://www.zhihu.com/signin?next=%2F'
bg_img_path = r'bg_img.png'
slide_img_path = r'slide_img.png'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
}

class ShuiLiCrawler:
    def __init__(self):
        self.pw = sync_playwright().start()
        self.context = self.pw.webkit.launch(headless=False).new_context()
        self.page = self.context.new_page()
        self.page.goto(index_url)

    def close(self):
        self.page.close()
        self.context.close()
        logger.info('playwright关闭！即将退出程序！')

    def get_png(self, page_source):
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

    def move_to_slide(self):
        self.page.fill('//input[@name="username"]', '17792209843')
        self.page.click('//button[@class="Button CountingDownButton SignFlow-smsInputButton Button--plain"]')
        time.sleep(3)
        self.get_png(self.page.content())
        tracks = get_validate_param(bg_img_path, slide_img_path)


    def run(self):
        self.page.wait_for_timeout(3000)
        self.move_to_slide()
        self.page.wait_for_timeout(3000)
        self.close()

if __name__ == '__main__':
    t = ShuiLiCrawler()
    t.run()