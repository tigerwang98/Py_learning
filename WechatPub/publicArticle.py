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

class WeixinPub():
    def __init__(self):
        self.url_configs = URL_CONFIG
        self.header = HEADER
        self.list_base_url = LIST_BASE_URL
        self.detail_base_url = DETAIL_BASE_URL
        self.logger = logging
        self.sess = requests.Session()
        self.proxy = get_16yun()

    def get_start_url(self, name, page,):
        param = 'query=%s&_sug_type_=&s_from=input&_sug_=n&type=2&page=%s&ie=utf8' % (quote(name), page)
        url = self.list_base_url + param
        return url

    def get_list(self, url):
        resp = self.sess.get(url=url, headers=self.header, proxies=self.proxy)
        if resp.status_code == 200:
            resp.encoding = 'utf-8'
            text = resp.text
        else:
            text = ''
        return text

    def parse_list_detail(self, page_source):
        items = []
        logging.info('正在获取重定向url及相关参数... ...')
        html = etree.HTML(page_source)
        logging.info('正在解析列表页面元素... ...')
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
            item = [title, author, pubtime, abstract, final_url]
            items.append(item)
        return items

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

    def get_detail(self, detailInfo_url):
        logging.info('开始请求详情页信息... ...')
        lua_script = '''
            function main(splash, args)
                url = "%s"
                assert(splash:go(url))
                assert(splash:wait(1))
                return {
                    html = splash:html(),
                }
                end
            ''' % detailInfo_url
        splash_url = SPLASH_URL + quote(lua_script)
        res = requests.get(url=splash_url)
        return res.json()['html']

    def parse_detail(self, detail_info):
        return detail_info

    def run(self):
        logging.info('开始读取作者列表... ...')
        with open(self.url_configs, 'r', encoding='utf-8') as f:
            authors = f.readlines()
        logging.info('作者列表读取成功！')
        author = authors.pop(0).strip('\n') if len(authors) > 0 else self.quit()
        for pg in range(PAGE):
            logging.info('开始获取%s公众号的第%s页' % (author, pg+1))
            url = self.get_start_url(author, page=(pg+1))
            logging.info('当前的列表页url是%s' % url)
            time.sleep(3)
            logging.info('开始解析当前页面... ...')
            page_source = self.get_list(url=url)
            datas = self.parse_list_detail(page_source)
            for data in datas:
                res = self.get_detail(data[-1])
                info = self.parse_detail(res)
                item = {'title': data[0], 'author': data[1], 'pubtime': data[2], 'abstract': data[3], 'url': data[4], 'info': info}
                yield item

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

    def close(self):
        logging.info('爬虫结束！')
        sys.exit(0)


'''
if __name__ =='__main__':
    logging.info('公众号爬虫开始！')
    spider = WeixinPub()
    datas = spider.run()
    while True:
        try:
            data = next(datas)
            if data:
                print(data)
        except StopIteration:
            break
    logging.info('公众号爬虫结束！')'''