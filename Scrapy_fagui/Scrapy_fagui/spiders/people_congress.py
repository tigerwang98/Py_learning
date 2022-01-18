import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import logging
import re
import time
from dateparser import parse
from urllib.parse import urlencode
import json

class PeopleCongressSpider(CrawlSpider):
    name = 'people_congress'
    allowed_domains = ['npc.gov.cn', 'flk.npc.gov.cn']
    start_urls = ['http://www.npc.gov.cn/']

    rules = (
        Rule(LinkExtractor(allow=r'c\d+/\d+/\w+\.shtml'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'.+list.*\.shtml'), callback='parse_list', follow=True),
        Rule(LinkExtractor(allow=r'flk.npc.gov.cn'), callback='generate_flk_list', follow=False),
        Rule(LinkExtractor(allow=r'detail2.html\?\w+'), callback='parse_flfg', follow=True),
    )

    def parse_item(self, response):
        title = "".join(response.xpath('//div[@class="tit"]/h1//text()').extract())
        if not title:
            title = "".join(response.xpath('//div[@class="tit"]/h2//text()').extract())
        pub_time = re.search('\d{4}(年|-|\.)\d{1,2}(月|-|\.)\d{1,2}', response.text).group()
        pubtime = self.get_standard_pubtime(pub_time)
        title = self.get_standard_title(title)
        author = '全国人大常委会'
        maker = '全国人大常委会'
        datatype = '解读'
        area_id = 1
        city_id = 1
        url = response.url
        info = response.xpath('//body').get()
        add_time = int(time.time())
        item = {'title': title, 'pubtime': pubtime, 'author': author, 'type': datatype,
                'maker': maker, 'notify_code': '', 'url': url, 'area_id': area_id,
                'city_id': city_id, 'info': info, 'add_time': add_time}
        filter_pattern = r'规则|规定|管理办法|法规|政策'
        if not re.search(filter_pattern, title):
            return
        return item

    def parse_list(self, response):
        for index in range(1, 5):
            next_page = response.url.replace('index.html', 'index_%s.html' % index)
            yield scrapy.Request(url=next_page)

    def generate_flk_list(self, response):
        url_list = {
            '宪法': '',
            '法律': {'param': 'flfg', 'page': 60},
            '行政法规': {'param': 'xzfg', 'page': 68},
            '监察法规': {'param': 'jcfg', 'page': 1},
            '司法解释': {'param': 'sfjs', 'page': 79},
            '地方性法规': {'param': 'dfxfg', 'page': 1740}
        }
        for moudle, v in url_list.items():
            param = {
                'searchType': 'title;accurate',
                'sortTr': 'f_bbrq_s;desc',
                'gbrqStart': '',
                'gbrqEnd': '',
                'sxrqStart': '',
                'sxrqEnd': '',
                'sort': 'true',
                'size': 10,
            }
            if moudle == '宪法':
                url = 'https://flk.npc.gov.cn/xf.html'
                yield scrapy.Request(url=url)
            else:
                param['type'] = list(v.values())[0]
                page_num = list(v.values())[1]
                for page in range(1, page_num):
                    param['page'] = page
                    param['_'] = int(time.time()*1000)
                    url = 'https://flk.npc.gov.cn/api/?' + urlencode(param)
                    print('url:')
                    print(url)
                    yield scrapy.Request(url=url, callback=self.parse_flk_list)

    def parse_flk_list(self, response):
        result = json.loads(response.text)
        for li in result['result']['data']:
            maker = li['office']
            pub_time = li['publish']
            title = li['title']
            datatype = li['type']
            url = li['url']
            pubtime = self.get_standard_pubtime(pub_time)
            title = self.get_standard_title(title)
            info = self.get_detail_info(url)
            add_time = int(time.time())
            item = {'title': title, 'pubtime': pubtime, 'author': '全国人大常委会', 'type': datatype, 'maker': maker,
                    'notify_code': '', 'url': url, 'area_id': 1, 'city_id': 1, 'info': info, 'add_time': add_time}
            yield item

    def get_detail_info(self, url):
        return 'KONG'

    def get_standard_pubtime(self, pub_time, normalize=False):
        if not isinstance(pub_time, str):
            try:
                pub_time = str(pub_time)
            except Exception as e:
                print(e)
                raise TypeError
        if pub_time.strip() == '-' or pub_time == '':
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