import requests
from playwright.sync_api import sync_playwright
import logging

logger = logging
logging.basicConfig(level=logging.INFO)

index_url = 'http://xypt.mwr.cn/'
url = 'http://xypt.mwr.cn/UnitCreInfo/listCydwPage.do?TYPE=1&amp;yzmCode='

class ShuiLiCrawler:
    def __init__(self):
        self.pw = sync_playwright().start()
        self.context = self.pw.webkit.launch(headless=False).new_context()
        self.init_fingerprint()

    def init_fingerprint(self):
        index_page = self.context.new_page()
        index_page.goto(index_url)
        index_page.wait_for_timeout(10000)
        self.page = self.context.new_page()
        self.page.goto(url)
        index_page.close()

    def parse_page(self):
        pass

    def insert_data(self, data):
        sql = ''''''

    def close(self):
        self.page.close()
        self.context.close()
        logger.info('playwright关闭！即将退出程序！')

    def run(self):
        self.page.wait_for_timeout(5000)
        self.page.click('xpath=//ul[@class="pagination pull-right no-margin"]//li/a[@onclick="nextPage(2)"]')
        self.page.wait_for_timeout(3000)
        print(self.page.content())
        self.close()

if __name__ == '__main__':
    t = ShuiLiCrawler()
    t.run()