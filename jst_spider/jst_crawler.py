import time
import requests
from hyper.contrib import HTTP20Adapter
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

class Driver():
    def __init__(self, driver_path, base_url, cookie):
        self.driver = webdriver.Chrome(driver_path)
        self.driver.add_cookie(cookie)
        self.driver.get(base_url)
        page_source = self.driver.page_source
        time.sleep(5)
        print(page_source)
        self.driver.quit()


def parse_info(text):
    html = etree.HTML(text)
    count = 0
    for item in html.xpath('//div[@class="table-con"]'):
        count += 1
        people = item.xpath('./ul/li[2]/a/text()')[0]
        company = item.xpath('./dl/dd[1]/a/text()')[0]
        pubtime = item.xpath('./dl/dd[3]/text()')[0]
        people = people.split('被评为')[0]
        print('%s.%s'%(count,people), company, pubtime, sep='||')



if __name__ == "__main__":
    driver_path = r'./chromedriver_win32/chromedriver.exe'
    url = 'https://www.cbi360.net/hhb/redlist/?pageindex=10&title=%E4%B8%AD%E7%9F%B3%E5%8C%96%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE%E4%BC%98%E7%A7%80%E9%A1%B9%E7%9B%AE%E7%BB%8F%E7%90%86&categoryids=c12g10a289&active=1&layer=true'
    # driver = Driver(driver_path, url, cookie)
    header = {
        'cookie': 'BAIDU_SSP_lcr=https://www.baidu.com/baidu.php?sc.K60000avpXkFvm720AcKTUte6LhEEcpPyyXR7MIdEsPpd0FjFrRm3l3fW4w4_NIzoLKRcmMyww_Nddd-EW9TtvXhXMBEGdlUkuExfWgpduplSvXrmYjMOky9_tN_2xheNJR9MKVaGZ-iF5PO_0LHXsCNwzMfArXlISl1FmZAxy5-ikDVuMKbX1a7Z96EsQZqCgWHAU5LZPMIid69SWu_5M_NilP-.7b_NR2Ar5Od663rj6tCULtXh1ssNNgsI4blY1FhmzkYnqerQKMks4tXrZofmzyuQQrPx7mhrzz1FuYtxZ-lXNzI5QIJyAp7WIbePhwf.U1Yk0ZDqEpWFlnvC0ZKGm1Yk0ZK1pyI85yn4ryP-uHKhPHnYm1PhPHb4Pyc4PAubn1-WPhNBnyNb0ZfqEpWFlnvC0A-V5HczPfKM5yq-TZnk0ZNG5yF9pywdUAY0TA-b5Hc30APGujYznWm0UgfqnH0krNtknjDLg1c3rHFxrjmzrNt1PW0k0AVG5H00TMfqPWc0mhbqnHRdg1Ddr7tznjwxnWDLg1RsnsKVm1Yknj0kg1D4njbYnjRsP1IxnH63PjT1Pj0sPHFxn7ts0Z7spyfqn0Kkmv-b5H00ThIYmyTqn0K9mWYsg100ugFM5H00TZ0qn0K8IM0qna3snj0snj0sn0KVIZ0qn0KbuAqs5H00ThCqnfKbugmqTAn0uMfqn0KspjYs0Aq15H00mMTqnH00UMfqn0K1XWY0mgPxpywW5yfvQyIlpZ940A-bm1dcHbc0TA9YXHY0IA7zuvNY5Hm1g1KxnHRs0ZwdT1Ydn1TdnjD1nj0dnjn4rHcvn1TL0ZF-TgfqnHmznW03n1DknWcLP6K1pyfqryn4uyDkPvRsnjFbPH-9r0KWTvYqfH64Pj6zP1DznW9KwHwjw6K9m1Yk0ZK85H00TydY5H00Tyd15H00XMfqn0KVmdqhThqV5HKxn7tsg1Kxn0Kbmy4dmhNxTAk9Uh-bT1Ysg1Kxn7tsg100TA7Ygvu_myTqn0Kbmv-b5H00ugwGujYVnfK9TLKWm1Ys0ZNspy4Wm1Ys0Z7VuWYs0AuWIgfqn0KGTvP_5H00mywhUA7M5HD0UAuW5H00uAPWujdAwWNDfYm3fRuDwjfLwjTYPHPDPWF7nWwanYczPj6sPfKYTh7buHYLrH0knjD0mhwGujdDfRN7nDFjrR7KwH9Kwjcdwj0zPjT3rDDvP1mLPDD4P6KBIjYs0Aq9IZTqn0KEIjYs0AqzTZfqnanscznsc10WnansQW0snj0snansc10WnanVc108nj0snj0sc1D8nj0snj0s0Z91IZRqrHm4nWTknfKkgLmqna33P-tsQW0sg108njKxna3zn-tsQWf3g108rjNxna3vP7tknW60mMPxTZFEuA-b5H00ThqGuhk9u1Ys0APv5fKGTdqWTADqn0KWTjYs0AN1IjYs0APzm1YknWnYns&xst=m1dAwWNDfYm3fRuDwjfLwjTYPHPDPWF7nWwanYczPj6sPf7B5RwKwRRsfbn4fR77rD7DnWNDnjcYP163fHmLPWTYfHbv0gnqnHDzrjRvn1RzP16LP1T4PWf4PW9xnWcdg10KI1vqJnMC1p6KTHvqJnMC1p6KIHY4PWbzP1Dk0gfqnHmznW03n1Dkn67VTHYs0W0aQf7WpjdhmdqsmsD1njDsP1Dkrjf3&word=&ck=6755.4.69.348.156.420.252.119&shh=www.baidu.com&sht=40020637_6_oem_dg&us=1.0.1.0.1.302.0&wd=&bc=110101; UM_distinctid=1787e034266958-0a26e5efe05976-c791039-17f408-1787e034267bde; ad_s_v_t_0323=4; cbi360_localization=false; ad_s_u_t_0323=5; ad_lb_u_t_0402=6; CNZZDATA30043621=cnzz_eid%3D339163285-1617262512-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1619312350; Hm_lvt_63840b7a7676718df8e92b28711649bd=1618313603,1619315394,1619316894,1619505569; cbi360_province=%e5%9b%9b%e5%b7%9d; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%229279b314-9562-4c5e-bf37-8fbb9f72a7af%22%2C%22first_id%22%3A%221787e0346724b0-07dbd2b6b2209a-c791039-1569800-1787e034673af9%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%7D%2C%22%24device_id%22%3A%221787e0346724b0-07dbd2b6b2209a-c791039-1569800-1787e034673af9%22%7D; CNZZDATA30036250=cnzz_eid%3D1199101605-1617016983-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1620800138; ad_lb_v_t_0422=2; ad_lb_u_t_0422=13; Hm_lvt_680d256f97e094a807ba2e598bd502f9=1621232887,1621309262,1621473151,1622083115; Hm_lvt_9f1a930c5ecc26fe983d898c26bd5fea=1621232887,1621309262,1621473151,1622083115; ad_s_v_t_0517=2; cbi360=accesstoken=F22E55C72A4356811EEA24FC8F7CE134060C43CE7A58D38F1CCBFCDFA577E8E42F17AD04B29FE86C263E2C1166CEC48379F1E3CB42408E89&expiretime=2021-09-24&ishistoryvip=0&isvip=1&nickname=tanzhuo&parentuseraccount=17313022663&parentuserid=01C95D91D5715028396AEC1AF480FEC46A52B61D67584DE6D76477EE882D7F2844E77E7E5C42841C&province=%e5%9b%9b%e5%b7%9d&sign=892e2d6a922f3c50&token=baea211da318485caa3a61e37574e949&uid=e8e9a3b90156e212&uidsign=90db445a443c0fb3&useraccount=17313022663&userid=01C95D91D5715028396AEC1AF480FEC46A52B61D67584DE6D76477EE882D7F2844E77E7E5C42841C&username=tanzhuo&viplevel=|10|&wxlogin=False; cbi360_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOiIwMUM5NUQ5MUQ1NzE1MDI4Mzk2QUVDMUFGNDgwRkVDNDZBNTJCNjFENjc1ODRERTZENzY0NzdFRTg4MkQ3RjI4NDRFNzdFN0U1QzQyODQxQyIsInVzZXJhY2NvdW50IjoiMTczMTMwMjI2NjMiLCJ1c2VycGhvbmUiOiIxNzMxMzAyMjY2MyIsImlhdCI6MTYyMjA4MzE4MX0.EKL_Mys3AX2p9U75bi9nskQyTsDPz8LBePG8UZ_w90k; Hm_lvt_2c83b793310ff6a04ed72f97dfc92eb9=1621473151,1621473184,1622083115,1622083182; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%229279b314-9562-4c5e-bf37-8fbb9f72a7af%22%2C%22first_id%22%3A%221787e0346724b0-07dbd2b6b2209a-c791039-1569800-1787e034673af9%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%7D%2C%22%24device_id%22%3A%221787e0346724b0-07dbd2b6b2209a-c791039-1569800-1787e034673af9%22%7D; ad_s_u_t_0517=7; ad_s_u_m_0517=true; Hm_lpvt_9f1a930c5ecc26fe983d898c26bd5fea=1622100981; Hm_lpvt_680d256f97e094a807ba2e598bd502f9=1622100981; Hm_lpvt_2c83b793310ff6a04ed72f97dfc92eb9=1622100981',
        'referer': 'https://www.cbi360.net/hhb/redlist/?pageindex=9&title=%E4%B8%AD%E7%9F%B3%E5%8C%96%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE%E4%BC%98%E7%A7%80%E9%A1%B9%E7%9B%AE%E7%BB%8F%E7%90%86&categoryids=c12g10a289&active=1&layer=true',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        ":authority": 'www.cbi360.net',
        ":method": 'GET',
        ":path": '/hhb/redlist/?pageindex=10&title=%E4%B8%AD%E7%9F%B3%E5%8C%96%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE%E4%BC%98%E7%A7%80%E9%A1%B9%E7%9B%AE%E7%BB%8F%E7%90%86&categoryids=c12g10a289&active=1&layer=true',
        ':scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
    }
    session = requests.session()
    session.mount('https://www.cbi360.net/hhb/redlist', HTTP20Adapter())
    res = session.get(url=url, headers=header)
    if res:
        res.encoding = 'utf-8'
        parse_info(res.text)
        # parse_info(res.text)