import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from playwright.sync_api import sync_playwright

index_url = r'http://xypt.mwr.cn/'
url = r'http://xypt.mwr.cn:80/UnitCreInfo/listCydwPage.do'
# url = r'https://www.baidu.com/'

def selenium_method():
    driver_path = r'C:\\Users\\Administrator\\Desktop\\Py_learning\\chromedriver_win32\\chromedriver.exe'
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(executable_path=driver_path, options=option)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })
    driver.get(url)
    time.sleep(10)
    driver.quit()

def use_playwright():
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=False)
        context = browser.new_context()
        page_index = context.new_page()
        page_index.goto(index_url)
        page_index.wait_for_timeout(5000)
        page = context.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)
        print(page.content())
        page.click('xpath=//table/tbody/tr[1]/td[2]/a')
        page.wait_for_timeout(5000)

        page_index.close()
        page.close()
        context.close()
        browser.close()
#
if __name__ == '__main__':
    use_playwright()

# def handle_page(page):
#     page.wait_for_load_state()
#     print(page.title())