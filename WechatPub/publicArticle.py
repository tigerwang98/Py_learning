# encoding: utf-8
"""
@project = Py_learing
@file = publicArticle
@author= wanghu
@create_time = 2021/8/18 16:35
"""
import execjs
import re
import logging
import requests
import json,time,sys
from urllib.parse import quote,urlencode
from dateparser import parse
from WechatPub.CONFIG import *
from lxml import etree
logging.basicConfig(level=logging.INFO)

proxy_host = "u5694.20.tp.16yun.cn"
proxy_port = "6447"
proxy_user = "16NPHKSJ"
proxy_pass = "287149"
logging.basicConfig(level=logging.INFO)

class WeixinPub():
    def __init__(self):
        self.url_configs = URL_CONFIG
        self.header = HEADER
        self.list_base_url = LIST_BASE_URL
        self.detail_base_url = DETAIL_BASE_URL
        self.page = PAGE
        self.logger = logging
        self.sess = requests.Session()
        self.proxy = self.get_16yun()

    def get_16yun(self):
        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxy_host,
            "port": proxy_port,
            "user": proxy_user,
            "pass": proxy_pass,
        }
        proxies = {
            "https": proxyMeta
        }
        return proxies

    def get_cur_url(self, name, page,):
        param = 'query=%s&_sug_type_=&s_from=input&_sug_=n&type=2&page=%s&ie=utf8' % (quote(name), page)
        url = self.list_base_url + param
        return url

    def send_request(self, url):
        resp = self.sess.get(url=url, headers=self.header)
        if resp.status_code == 200:
            resp.encoding = 'utf-8'
            text = resp.text
        else:
            text = ''
        return text

    def get_detail_url(self, param_url):
        final_url = ''
        pattern = r'url \+= \'.*\';'
        url = param_url + '&k=64&h=F'
        resp = self.sess.get(url=url, headers=self.header)
        resp.encoding = resp.apparent_encoding
        for href in re.findall(pattern, resp.text):
            url_str = href.split('+=')[-1].strip()[:-1].strip('\'')
            final_url += url_str
        return final_url

    def parse_detail(self, page):
        logging.info('正在获取重定向url及相关参数... ...')
        time.sleep(2)
        html = etree.HTML(page)
        logging.info('正在解析页面元素... ...')
        for li in html.xpath('//ul[@class="news-list"]//li'):
            title = li.xpath('./div[@class="txt-box"]//h3/a//text()')[0]
            try:
                abstract = li.xpath('.//p[@class="txt-info"]//text()')[0]
            except IndexError:
                abstract = ''
            pub_time = li.xpath('.//div[@class="s-p"]//span[@class="s2"]//text()')[0]
            pubtime = self.get_standard_pubtime(pub_time)
            author = li.xpath('.//div[@class="s-p"]//a[@class="account"]//text()')[0]
            href = li.xpath('./div[@class="txt-box"]//h3/a/@href')[0]
            url = href if href.startswith('http') else LIST_BASE_URL + href
            final_url = self.get_detail_url(url.replace('weixin?/', ''))
            print(title, author, pubtime, abstract, final_url)

    def run(self):
        logging.info('开始读取作者列表... ...')
        with open(self.url_configs, 'r', encoding='utf-8') as f:
            authors = f.readlines()
        logging.info('作者列表读取成功！')
        author = authors.pop(0) if len(authors) > 0 else self.quit()
        for pg in range(self.page):
            logging.info('开始获取%s公众号的第%s页' % (author, pg+1))
            url = self.get_cur_url(author, page=(pg+1))
            logging.info('当前的列表页url是%s' % url)
            time.sleep(3)
            logging.info('开始解析当前页面... ...')
            page_source = self.send_request(url=url)
            datas = self.parse_detail(page=page_source)
            yield datas

    def get_standard_pubtime(self, pub_time):
        if not isinstance(pub_time, str):
            try:
                pub_time = str(pub_time)
            except Exception as e:
                print(e)
                raise TypeError
        param_time = re.search(r'\("\d+"\)', pub_time.replace('\'', '"')).group()
        pub_time = param_time.replace('(', '').replace(')', '').strip('"')
        if pub_time.strip() == '-':
            return '-'
        pub_time = re.sub(r'\\r|\\n|\\t', '', pub_time)
        pubtime = parse(pub_time)
        if pubtime:
            return str(pubtime).split(' ')[0]
        else:
            self.logger.info('%s 时间格式不对！' % pub_time)
            return TypeError

    def quit(self):
        print('here')
        sys.exit(0)

if __name__ =='__main__':
    logging.info('公众号爬虫开始！')
    spider = WeixinPub()
    datas = spider.run()

