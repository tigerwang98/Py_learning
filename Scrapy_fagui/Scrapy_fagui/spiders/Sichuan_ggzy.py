import json
import re
import time
from urllib.parse import urlencode
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from dateparser import parse
from scrapy.loader import ItemLoader
from Scrapy_fagui.Scrapy_fagui.items import ScrapyFaguiItem
from ..loaders import DetailItemLoader
from scrapy_splash import SplashRequest

class SichuanGgzySpider(CrawlSpider):
    name = 'Sichuan_ggzy'
    allowed_domains = ['ggzyjy.sc.gov.cn']
    start_urls = ['http://ggzyjy.sc.gov.cn/']

    rules = (
        Rule(LinkExtractor(allow=r'xwzx/(\w+/){0,2}.*more', deny=r'\w-\w'), callback='generate_page', follow=True),
        Rule(LinkExtractor(allow=r'jyxx/transactionInfo'), callback='generate_page', follow=True),
        Rule(LinkExtractor(allow=r'ycpb/moreinfomenu'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'bszn/bsznnotice'), callback='generate_page', follow=True),
        Rule(LinkExtractor(allow=r'zcfg/moreinfo'), callback='generate_zcfg_page', follow=True),
        Rule(LinkExtractor(allow=r'cyzdxm/transactionInfocyzd'), callback='generate_page', follow=True),
        Rule(LinkExtractor(allow=r'#/secondHome.html'), callback='generate_pbzjk_page', follow=True),
        Rule(LinkExtractor(allow=r'cxgl/sincerity-creditinfo'), callback='generate_cxjd', follow=True),
        Rule(LinkExtractor(allow=r'(\w+/)+(\w+-\w+)+.html'), callback='parse_detail_item', follow=True),
    )

    def generate_page(self, response):
        for page in range(2, 6):
            url = response.url[:response.url.rindex('/')] + '/{}.html'.format(page)
            yield scrapy.Request(url=url, callback=self.parse_item)

    def generate_zcfg_page(self, response):
        for page in range(2, 6):
            url = response.url[:response.url.rindex('/')] + '/{}.html'.format(page)
            yield scrapy.Request(url=url, callback=self.parse_zcfg_item)

    def generate_pbzjk_page(self, repsonse):
        param = {
            '_': int(time.time()),
            'limit': 10,
            'title': '',
            'publishBeginTime': '',
            'publishEndTime': '',
        }
        for noticetype in range(6):
            if noticetype == 0:
                base_url = 'http://ggzyjy.sc.gov.cn:81/api/portalindex/collect/list?'
                for page in range(1, 6):
                    param['page'] = page
                    url = base_url + urlencode(param)
                    yield scrapy.Request(url=url, callback=self.parse_pbzjks, meta={'type': 6})
                continue
            if noticetype == 5:
                base_url = 'http://ggzyjy.sc.gov.cn:81/api/portalindex/train/list?'
            else:
                base_url = 'http://ggzyjy.sc.gov.cn:81/api/portalindex/work/list?'
            param['noticeType'] = noticetype
            for page in range(1, 6):
                param['page'] = page
                url = base_url + urlencode(param)
                yield scrapy.Request(url=url, callback=self.parse_pbzjks, meta={'type': noticetype})

    def generate_cxjd(self, response):
        url = 'http://ggzyjy.sc.gov.cn/WebBuilder/rest/credit/getList'
        for page in range(5):
            param = {
            "name": "",
            "code": "",
            "type": "00",
            "sttime": "",
            "endtime": "",
            "pageSize": '15',
            "index": str(page),
        }
            yield scrapy.FormRequest(url=url, formdata=param, callback=self.parse_cxjd)

    def parse_zcfg_item(self, response):
        for li in response.xpath('//ul[@class="policylist"]//li'):
            href = li.xpath('./a/@href').extract_first()
            title = li.xpath('./a//text()').extract_first()
            pub_time = li.xpath('./span[@class="date"]//text()').extract_first()
            pubtime = self.get_standard_pubtime(pub_time)
            url = response.urljoin(href)
            item = {'title': title, 'pubtime': pubtime, 'url': url}
            yield scrapy.Request(url=url, meta=item, callback=self.get_item)

    def parse_item(self, response):
        for li in response.xpath('//ul[@class="comm-list"]//li'):
            loader = DetailItemLoader(item=ScrapyFaguiItem(), response=response)
            loader.add_xpath('title', '')
            title = li.xpath('./p/a//text()')
            href = li.xpath('./p/a/@href').extract_first()
            url = response.urljoin(href)
            pubtime = li.xpath('./p/span//text()').extract_first()
            author = li.xpath('./span/i/text()').extract_first()
            item = {'title': title, 'pubtime': pubtime, 'author': author, 'url': url}
            yield scrapy.Request(url=url, meta=item, callback=self.get_item)

    def parse_pbzjks(self, response):
        type = response.meta['type']
        base_url = 'http://ggzyjy.sc.gov.cn:81/'
        results = json.loads(response.text)
        for result in results['data']:
            title = result['title']
            pub_time = result.get('publishtime')
            if not pub_time:
                pub_time = result.get('fpublishtime')
            if not pub_time:
                pub_time = result.get('publishTime')
            data_id = result['id']
            pubtime = self.get_standard_pubtime(pub_time)
            url = base_url + '#/NewsDetail?id=' + data_id + '&type=' + str(type)
            item = {'title': title, 'pubtime': pubtime, 'url': url}
            yield scrapy.Request(url=url, meta=item, callback=self.get_item, dont_filter=True)

    def parse_cxjd(self, response):
        '''
        返回的数据有????
        :param response:
        :return:
        '''
        results = json.loads(response.body.decode('utf-8'))
        for result in results['creditinfo']:
            title = result['legal_name']
            pub_time = result['operatedate']
            com_code = result['legal_code']
            role = result['legal_role']
            institution = result['r_pfcode']
            href = result['rowguid']
            pubtime = self.get_standard_pubtime(pub_time)
            print(title, com_code, role, pubtime, institution, href)

    def get_item(self, response):
        loader = ItemLoader(item=ScrapyFaguiItem(), response=response)
        loader.add_xpath('info', '//div[contains(@class, "news-detailed")]')
        data = response.meta

        for k, v in data.items():
            loader.add_value(k, v)
        loader.add_value('area_id', 26)
        loader.add_value('city_id', 0)
        loader.add_value('author', '四川省公共资源交易网')
        return loader.load_item()

    def parse_detail_item(self, response):
        infos = response.xpath('//div[contains(@class, "news-detailed")]').get()
        title = response.xpath('//h2[@class="detailed-title"]//text()').get()
        pub_time = re.search('\d{4}(年|-|\.)\d{1,2}(月|-|\.)\d{1,2}', response.text).group()
        pubtime = self.get_standard_pubtime(pub_time)
        author = '四川省公共资源交易网'
        area_id = 26
        city_id = 0
        if not infos:
            infos = '没有info!'
        item = {'title': title, 'pubtime': pubtime, 'author': author,
                'area_id': area_id, 'city_id': city_id, 'info': infos, 'url': response.url}
        return item

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
            return '-'