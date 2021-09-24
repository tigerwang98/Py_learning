import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from dateparser import parse
import time
from lxml import etree
from .xpath_list import *
from ..items import CrawlspiderTestItem
from ..settings import ERR_LOG_PATH
import logging

class SichuanEnvironmentSpider(CrawlSpider):
    name = 'Sichuan_environment'
    allowed_domains = ['sthjt.sc.gov.cn',]
    start_urls = ['http://sthjt.sc.gov.cn/sthjt/index.shtml',]

    def __init__(self, *args, **kwargs):
        super(SichuanEnvironmentSpider, self).__init__(*args, **kwargs)

    rules = (
        # 中转链接模块
        Rule(LinkExtractor(allow=r'http://sthjt.sc.gov.cn/.*/.*/.?jump\.shtml'), callback='parse_jump', follow='True'),
        # 新闻类，政策类
        Rule(LinkExtractor(allow=r'http://sthjt.sc.gov.cn/.*/\w+/\d{1,4}/\d{1,2}/\d{1,2}/.*\.shtml'),
             callback='parse_detail', follow=True),
        # 列表页
        Rule(LinkExtractor(allow=r'http://sthjt.sc.gov.cn/sthjt/.*list.*\.shtml'), callback='parse_list', follow=True),
        # 政府信息公开模块等一些其他非规则模块
        Rule(LinkExtractor(allow=r'http://sthjt.sc.gov.cn/.*/\w+/.*\.shtml'), callback='parse_list', follow=True),
    )

    def parse_jump(self, response):
        selector = scrapy.Selector(response)
        moudle_url = selector.xpath('//p[@id="url"]')[0].get()
        url = 'http://sthjt.sc.gov.cn' + moudle_url
        yield scrapy.Request(url=url)

    def parse_list(self, response):
        for index in range(1, 3):
            next_page = response.url.split('.shtml')[0] + '_%s' % index + '.shtml'
            yield scrapy.Request(url=next_page)

    def parse_detail(self, response):
        item = CrawlspiderTestItem()
        selector = scrapy.Selector(response)
        item_dict = {}
        for k, xpath_list in xpath_dict.items():
            for item_xpath in xpath_list:
                try:
                    item_dict[k] = selector.xpath(item_xpath)[0].get()
                except IndexError:
                    continue
                else:
                    break
        try:
            pubtime = re.search(r'\d{1,4}(年|-|\.)\d{1,2}(月|-|\.)\d{1,2}', item_dict['pub_time']).group()
            std_pubtime = self.get_standard_pubtime(pubtime)
            std_title = self.get_standard_title(item_dict['title'])
            infos = item_dict['infos']
        except Exception as e:
            with open(ERR_LOG_PATH, 'a+', encoding='utf-8') as f:
                err_info = 'spiderName:%s\nurl:%s\nreason:%s\ntime:%s\n' % ('四川生态环境厅', response.url, e, time.strftime('%Y-%M-%D %H:%M:%S'))
                f.write(err_info)
                std_title = ''
                std_pubtime = ''
                infos = ''
                logging.info('发现有xpath未覆盖的数据！')
            return None
        author = '四川省生态环境厅'
        outurl = response.url
        file_list =self.get_file_list(item_dict['infos'], outurl)
        file_url = ",".join(f['file_url'] for f in file_list)
        add_time = int(time.time())
        item['title'] = std_title
        item['pubtime'] = std_pubtime
        item['area_id'] = 26
        item['city_id'] = 1
        item['author'] = author
        item['url'] = outurl
        item['add_time'] = add_time
        item['info'] = infos
        item['file_url'] = file_url
        return item

    def get_standard_pubtime(self, pub_time):
        if not isinstance(pub_time, str):
            raise TypeError
        if pub_time.strip() == '-':
            return '-'
        pub_time = re.sub(r'\\r|\\n|\\t', '', pub_time)
        pubtime = parse(pub_time)
        if pubtime:
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

    def get_file_list(self, html, curPage_url):
        part_html = etree.HTML(html)
        file_list = []
        filter_file_url_set = set()
        houzhui_list = ['pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx']
        base_url = curPage_url[:curPage_url.rindex('/')]
        xpath_list = ['.//a/@href', './/img/@src', './/embed/@src']
        for xpath in xpath_list:
            file_url_list = part_html.xpath(xpath)
            if len(file_url_list) > 0:
                for file_url in file_url_list:
                    houzhui = file_url.split('.')[-1]
                    if houzhui in houzhui_list:
                        final_url = 'http://sthjt.sc.gov.cn' + file_url if '/sthjt/' in file_url else base_url + '/' + file_url
                        file_data = {'file_name': 'title.' + houzhui, 'file_url': final_url}
                        if not filter_file_url_set.add(final_url):
                            file_list.append(file_data)
        return file_list