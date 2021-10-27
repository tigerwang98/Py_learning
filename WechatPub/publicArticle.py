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
from .common_tool import chromeTorender
from .dupfilter_data import filter_data

logging.basicConfig(level=logging.DEBUG)

class WeixinPub():
    def __init__(self):
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
            title = "".join(li.xpath('./div[@class="txt-box"]//h3//text()')).strip('\n')
            try:
                abstract = "".join(li.xpath('.//p[@class="txt-info"]//text()'))
            except IndexError:
                abstract = ''
            pub_time = li.xpath('.//div[@class="s-p"]//span[@class="s2"]//text()')[0]
            pubtime = self.get_standard_pubtime(pub_time).split(' ')[0]
            author = li.xpath('.//div[@class="s-p"]//a[@class="account"]//text()')[0]
            href = li.xpath('./div[@class="txt-box"]//h3//a/@href')[0]
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
        retry_times = 0
        lua_script = '''
            function main(splash, args)
                url = "%s"
                assert(splash:go(url))
                assert(splash:wait(0.5))
                return {
                    html = splash:html(),
                }
                end
            ''' % detailInfo_url
        splash_url = SPLASH_URL + quote(lua_script)
        while True:
            retry_times += 1
            res = requests.get(url=splash_url)
            try:
                if len(res.json()['html']) > 100:
                    return res.json()['html']
            except KeyError:
                res = chromeTorender(detailInfo_url)
                return res
            if retry_times == 30:
                logging.info('请求splash渲染超时！请检查爬虫！')
                raise Exception
            logging.info('第%s次splash渲染失败！正在重试中... ...' % retry_times)

    def parse_detail(self, detail_info):
        html = etree.HTML(detail_info)
        try:
            infos = html.xpath('//div[@id="js_article"]')[0]
            info = etree.tostring(infos, encoding='utf-8').decode()
        except:
            info = None
            logging.info('内容可能被删除了!请检查url:')
        return info

    def run(self, author, pg):
        logging.info('开始获取%s公众号的第%s页' % (author, pg+1))
        url = self.get_start_url(author, page=(pg+1))
        logging.info('当前的列表页url是%s' % url)
        logging.info('开始解析当前页面... ...')
        page_source = self.get_list(url=url)
        datas = self.parse_list_detail(page_source)
        for data in datas:
            # 写入去重文件是否成功
            if not filter_data('Bloom', 'WechatPub', data[-1]):
                continue
            res = self.get_detail(data[4])
            info = self.parse_detail(res)
            if not info:
                logging.info(data[4])
                continue
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
