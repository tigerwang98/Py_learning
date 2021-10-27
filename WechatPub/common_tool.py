# encoding: utf-8
"""
@project = Py_learing
@file = drivertorender
@author= wanghu
@create_time = 2021/10/22 15:20
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

driver_path = r'C:\Users\123\Desktop\Py_learing\chromedriver_win32\\chromedriver.exe'
def chromeTorender(url):
    chrome_opt = Options()
    chrome_opt.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    )
    chrome_opt.add_argument(
        '--disable-blink-features=AutomationControlled'
    )
    chrome_opt.add_argument(
        '--headless'
    )
    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_opt)
    with open('stealth.min.js', 'r', encoding='utf-8') as f:
        js = f.read()
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })
    driver.get(url=url)
    html = driver.page_source
    driver.quit()
    return html

if __name__ == '__main__':
    url = 'https://mp.weixin.qq.com/s?src=3&timestamp=1634886468&ver=1&signature=-IdE9**yN6xIScHFEVGL6Y6B3vF478wN91GbmpkUCSLgvSnfoqY6N*IJRhcoylc9pGiRq5UuJm3KZR451OB7jJCSQCdsp*2Jhi5NlR3VBsnVaLgUUCaRI7QxzEouVkksXBjsTcosj0uf7KwYElhscg=='
    a = chromeTorender(url)
    with open('temp.html', 'w', encoding='utf-8') as f:
        f.write(a)