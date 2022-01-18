import json
import re
import time

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from dateparser import parse

class SichuanGovSpider(CrawlSpider):
    name = 'sichuan_gov'
    allowed_domains = ['www.sc.gov.cn']
    start_urls = ['http://www.sc.gov.cn/']

    rules = (
        Rule(LinkExtractor(allow=r'/10462/c103041/newzfwj.shtml'), callback='generate_zfwj', follow=True),
        Rule(LinkExtractor(allow=r'/10462/10464/13298/zcjd.shtml'), callback='generate_zcjd', follow=True),
        Rule(LinkExtractor(allow=r'/10462/c108923/zfgz_list.shtml'), callback='generate_zfgz', follow=True),
        Rule(LinkExtractor(allow=r'(/\w+)+\.shtml'), callback='parse_item', follow=True),
        )

    def parse_item(self, response):
        title = "".join(response.xpath('//div[@id="container"]//h2//text()').extract())
        if not title:
            title = "".join(response.xpath('//div[@id="container"]//h1//text()').extract())
        if not title:
            title = "".join(response.xpath('//div[@class="zfgztit"]//text()').extract())
        pub_time = re.search('\d{4}(年|-|\.)\d{1,2}(月|-|\.)\d{1,2}', response.text).group()
        pubtime = self.get_standard_pubtime(pub_time)
        title = self.get_standard_title(title)
        author = '四川省人民政府'
        maker = '四川省人民政府'
        datatype = '解读'
        area_id = 26
        city_id = 1
        url = response.url
        info = response.xpath('//body').get()
        add_time = int(time.time())
        item = {'title': title, 'pubtime': pubtime, 'author': author, 'type': datatype,
                'maker': maker, 'notify_code': '', 'url': url, 'area_id': area_id,
                'city_id': city_id, 'add_time': add_time}
        item['info'] = info
        filter_pattern = r'规则|规定|管理办法|法规|政策|决定|办法'
        if not re.search(filter_pattern, title):
            return
        return item

    def generate_zfwj(self, response):
        channelId_list = response.xpath('//div[@class="dhnav01 wzfl active"]/ul[@class="xl"]//li/@channelid').extract()
        api_url = 'http://www.sc.gov.cn/cms-scsrmzf/qryZFWJListByConditionsNew'
        header = {
            'Content-Type': 'application/json',
            'Referer': 'http://www.sc.gov.cn/10462/c103041/newzfwj.shtml'
        }
        maker_id = ['四川省人民政府', '四川省人民政府', '四川省人民政府', '四川省人民政府办公厅', '四川省人民政府办公厅']
        for index, channelid in enumerate(channelId_list):
            if index == 0:      page = 12
            elif index == 1:    page = 46
            elif index == 2:    page = 98
            elif index == 3:    page = 74
            else:               page = 66
            for pagenum in range(1, page+1):
                param = {
                    "keyWord": "", "wh": "", "fwzh": "", "pageSize": 10, "pageNum": pagenum,
                    "channelId": ["%s" % channelid]
                }
                yield scrapy.Request(url=api_url, headers=header, method='POST', body=json.dumps(param), callback=self.parse_zfwj, meta={'maker_id': maker_id[index]})

    def generate_zcjd(self, response):
        url_list = [
        'http://www.sc.gov.cn/10462/10464/13298/13299/zcjd_list.shtml',
        'http://www.sc.gov.cn/10462/10464/13298/14097/bmjd_list.shtml',
        'http://www.sc.gov.cn/10462/10464/13298/13303/rdjd_list.shtml',
        'http://www.sc.gov.cn/10462/10464/13298/14083/ldgd_list.shtml',
        ]
        for url in url_list:
            for page in range(2, 16):
                next_url = url.replace('list.shtml', 'list_%s.shtml' % page)
                yield scrapy.Request(url=next_url, callback=self.parse_zcjd)
            yield scrapy.Request(url=url, callback=self.parse_zcjd)

    def generate_zfgz(self, response):
        url = response.url
        for page in range(2, 12):
            next_page = url.replace('list', 'list_%s' % page)
            yield scrapy.Request(url=next_page, callback=self.parse_zfgz)

    def parse_zfwj(self, response):
        result = json.loads(response.text)
        for li in result['results']:
            url = li['url']
            pub_time = li['publishedTime']
            notify_code = li['wh']
            title = li['title']
            pubtime = self.get_standard_pubtime(pub_time)
            title = self.get_standard_title(title)
            maker_id = response.meta['maker_id']

            author = '四川省人民政府'
            datatype = '地方性法规'
            area_id = 1
            city_id = 1
            info = 'KONG'
            add_time = int(time.time())
            item = {'title': title, 'pubtime': pubtime, 'author': author, 'type': datatype,
                    'maker': maker_id, 'notify_code': notify_code, 'url': url, 'area_id': area_id,
                    'city_id': city_id, 'info': info, 'add_time': add_time}
            yield item

    def parse_zcjd(self, response):
        for tr in response.xpath('//table[@id="dash-table"]//tr'):
            title = tr.xpath('./td[2]//a/@title').extract_first()
            href = tr.xpath('./td[2]//a/@href').extract_first()
            url = 'http://www.sc.gov.cn/' + href
            yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_zfgz(self, response):
        for tr in response.xpath('//div[@class="yxgzul"]//li'):
            title = tr.xpath('.//div[@class="p1"]/a/@title').extract_first()
            href = tr.xpath('.//div[@class="p1"]/a/@href').extract_first()
            maker = tr.xpath('.//div[@class="p2"]//text()').extract_first().split('　')[0]
            url = 'http://www.sc.gov.cn/' + href
            pub_time = re.search('\d{4}(年|-|\.)\d{1,2}(月|-|\.)\d{1,2}', maker).group()
            pubtime = self.get_standard_pubtime(pub_time)
            maker_id = maker.split('日')[-1].replace('公布', '').replace('发布', '')

            author = '四川省人民政府'
            table_maker = '四川省人民政府'
            notify_code = maker_id
            datatype = '地方性法规'
            area_id = 1
            city_id = 1
            info = 'KONG'
            add_time = int(time.time())
            item = {'title': title, 'pubtime': pubtime, 'author': author, 'type': datatype,
                    'maker': table_maker, 'notify_code': notify_code, 'url': url, 'area_id': area_id,
                    'city_id': city_id, 'info': info, 'add_time': add_time}
            yield item

    def get_info(self, url):
        return 'info'

    def get_standard_pubtime(self, pub_time, normalize=False):
        if not isinstance(pub_time, str):
            try:
                pub_time = str(pub_time)
            except Exception as e:
                print(e)
                raise TypeError
        if pub_time.strip() == '-':
            return '-'
        pub_time = re.sub(r'\\r|\\n|\\t', '', pub_time)
        pubtime = parse(pub_time)
        if pubtime:
            standard_get_time = str(pubtime).split(' ')[0]
            standard_cur_time = time.strftime("%Y-%m-%d", time.localtime())
            get_time = int(time.mktime(time.strptime(standard_get_time, '%Y-%m-%d')))
            cur_time = time.time()
            if get_time > cur_time and normalize:
                return standard_cur_time
            return str(pubtime).split(' ')[0]
        else:
            self.logger.info('%s 时间格式不对！' % pub_time)
            raise TypeError

    def get_standard_title(self, title):
        if not isinstance(title, str):
            raise TypeError
        title = re.sub(r'\\r|\\n|\\t', '', title)
        if '【' in title or '】' in title:
            pattern = r'【.+?】'
            title = re.sub(pattern, '', title)
        title = self.filter_tags(title).strip()
        return title

    def filter_tags(self, htmlstr):
        # 先过滤CDATA
        re_cdata = re.compile('//<![CDATA[[^>]*//]]>', re.I)  # 匹配CDATA
        re_script = re.compile('<s*script[^>]*>[^<]*<s*/s*scripts*>', re.I)  # Script
        re_style = re.compile('<s*style[^>]*>[^<]*<s*/s*styles*>', re.I)  # style
        re_br = re.compile('<brs*?/?>')  # 处理换行
        re_h = re.compile('<[^>]+>')  # HTML标签
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        s = re_cdata.sub('', htmlstr)  # 去掉CDATA
        s = re_script.sub('', s)  # 去掉SCRIPT
        s = re_style.sub('', s)  # 去掉style
        s = re_br.sub('n', s)  # 将br转换为换行
        s = re_h.sub('', s)  # 去掉HTML标签
        s = re_comment.sub('', s)  # 去掉HTML注释
        # 去掉多余的空行
        blank_line = re.compile('n+')
        s = blank_line.sub('n', s)
        s = self.replaceCharEntity(s)  # 替换实体
        return s

        ##替换常用HTML字符实体.
        # 使用正常的字符替换HTML中特殊的字符实体.
        # 你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
        # @param htmlstr HTML字符串.

    def replaceCharEntity(self, htmlstr):
        CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                         'lt': '<', '60': '<',
                         'gt': '>', '62': '>',
                         'amp': '&', '38': '&',
                         'quot': '"', '34': '"', }

        re_charEntity = re.compile(r'&#?(?P<name>w+);')
        sz = re_charEntity.search(htmlstr)
        while sz:
            entity = sz.group()  # entity全称，如>
            key = sz.group('name')  # 去除&;后entity,如>为gt
            try:
                htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
            except KeyError:
                # 以空串代替
                htmlstr = re_charEntity.sub('', htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
        return htmlstr

    def repalce(self, s, re_exp, repl_string):
        return re_exp.sub(repl_string, s)