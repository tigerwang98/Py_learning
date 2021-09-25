import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ScrapyZixunItem
import time
from dateparser import parse
import re
from redis import Redis
import logging
from scrapy_redis.spiders import RedisSpider

class ChongqingFgwSpider(RedisSpider):
    name = 'Chongqing_fgw'
    allowed_domains = ['fzggw.cq.gov.cn']
    # start_urls = ['http://fzggw.cq.gov.cn/']
    redis_key = 'Chongqing_fgw'

    rules = (
        Rule(LinkExtractor(allow=r'.*\.html', deny=r'\./.*/.*'), callback='parse_detail', follow=False),
        Rule(LinkExtractor(allow=r'.*index.*\.html'), callback='parse_list', follow=True),
        Rule(LinkExtractor(allow=r'\./.*/.*'), callback='parse_jump', follow=True),
        Rule(LinkExtractor(allow=r''), callback='parse', follow=True),
    )

    def parse(self, response, **kwargs):
        pass

    def parse_jump(self, response):
        url = 'http://fzggw.cq.gov.cn/' + response.url[1:] + 'index.html'
        yield scrapy.Request(url=url)

    def parse_list(self, response):
        for index in range(1, 3):
            next_page = response.url.replace('index.html', 'index_%s.html' % index)
            yield scrapy.Request(url=next_page)

    def parse_detail(self, response):
        item = ScrapyZixunItem()
        pub_time = re.search(r'\d{1,4}(年|-|\.)\d{1,2}(月|-|\.)\d{1,2}', response.text).group()
        title = response.xpath('//p[@class="tit"]//text()')[0].get()
        infos = response.xpath('//div[@class="zwxl-article"]').get()
        author = '重庆市发展和改革委员会'

    # ---------------下面是固定代码----------------------------
        std_pubtime = self.get_standard_pubtime(pub_time)
        std_title = self.get_standard_title(title)
        outurl = response.url
        file_url = ''
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
    #--------------------------------------------------------