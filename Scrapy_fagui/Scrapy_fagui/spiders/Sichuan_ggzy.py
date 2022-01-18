import json
import re
import time
from urllib.parse import urlencode
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from dateparser import parse

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

    def parse_item(self, response):
        for li in response.xpath('//ul[@class="comm-list"]//li'):
            title = li.xpath('./p/a//text()').extract_first()
            href = li.xpath('./p/a/@href').extract_first()
            url = response.urljoin(href)
            pubtime = li.xpath('./p/span//text()').extract_first()
            author = li.xpath('./span/i/text()').extract_first()
            item = {'title': title, 'pubtime': pubtime, 'author': author, 'url': url}
            yield scrapy.Request(url=url, meta=item, callback=self.get_item)

    def generate_page(self, response):
        for page in range(2, 6):
            url = response.url[:response.url.rindex('/')] + '/{}.html'.format(page)
            yield scrapy.Request(url=url, callback=self.parse_item)

    def generate_zcfg_page(self, response):
        for page in range(2, 6):
            url = response.url[:response.url.rindex('/')] + '/{}.html'.format(page)
            yield scrapy.Request(url=url, callback=self.parse_zcfg_item)

    def parse_zcfg_item(self, response):
        for li in response.xpath('//ul[@class="policylist"]//li'):
            href = li.xpath('./a/@href').extract_first()
            title = li.xpath('./a//text()').extract_first()
            pub_time = li.xpath('./span[@class="date"]//text()').extract_first()
            pubtime = self.get_standard_pubtime(pub_time)
            url = response.urljoin(href)
            item = {'title': title, 'pubtime': pubtime, 'url': url}
            yield scrapy.Request(url=url, meta=item, callback=self.get_item)

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
            print(item)
            yield scrapy.Request(url=url, meta=item, callback=self.get_item, dont_filter=True)

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
            cookie = {
                'Cookie': 'JSESSIONID=7AF93A9CAEBCF332FB76A21A21837B96; yfx_c_g_u_id_10000001=_ck21032920393518150697265969215; yfx_key_10000001=; yfx_mr_10000001=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_c_g_u_id_10003074=_ck21032920393518874152611116407; yfx_key_10003074=; yfx_mr_10003074=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_c_g_u_id_10000040=_ck21091614431712645178348696470; UM_distinctid=17bed896039bf3-0a20a54b192697-4343363-17f408-17bed89603a5d4; yfx_c_g_u_id_10003095=_ck21091615364816218959707253432; yfx_f_l_v_t_10003095=f_t_1631777808626__r_t_1632446567073__v_t_1632446567073__r_c_4; yfx_f_l_v_t_10000040=f_t_1631774597256__r_t_1632728646588__v_t_1632728646588__r_c_5; yfx_key_10000040=; yfx_mr_10000040=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_c_g_u_id_10000009=_ck21092717191017498171238374501; yfx_f_l_v_t_10000009=f_t_1632734350739__r_t_1632734350739__v_t_1632734350739__r_c_0; yfx_key_10000009=; yfx_mr_10000009=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_c_g_u_id_10003036=_ck21092717191019964189121165335; yfx_f_l_v_t_10003036=f_t_1632734350991__r_t_1632734350991__v_t_1632734350991__r_c_0; yfx_key_10003036=; yfx_mr_10003036=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_c_g_u_id_10000042=_ck21100911452412354091123183975; userGuid=-2001935666; yfx_mr_f_10000001=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_mr_f_10003074=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_c_g_u_id_10000021=_ck22011115350510472501308581733; yfx_f_l_v_t_10000021=f_t_1641886505044__r_t_1641886505044__v_t_1641886505044__r_c_0; yfx_f_l_v_t_10000042=f_t_1633751124234__r_t_1641886916014__v_t_1641886916014__r_c_1; Hm_lvt_da7caec4897c6edeca8fe272db36cca4=1641868549,1641974192,1642036285; yfx_f_l_v_t_10000001=f_t_1617021575804__r_t_1642403766949__v_t_1642403766949__r_c_6; yfx_f_l_v_t_10003074=f_t_1617021575883__r_t_1642403769978__v_t_1642403769978__r_c_4; Hm_lpvt_da7caec4897c6edeca8fe272db36cca4=1642403910; CNZZDATA1276636503=1042341143-1635748204-%7C1642479253'
            }
            yield scrapy.FormRequest(url=url, formdata=param, cookies=cookie, callback=self.parse_cxjd)

    def parse_cxjd(self, response):
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

    def get_item(self, response):
        print('here')
        info = response.xpath('//div[contains(@class, "news-detailed")]').get()
        if not info:
            info = 'info为空!'
        item = response.meta
        item['info'] = info
        item['area_id'] = 26
        item['city_id'] = 0
        item['author'] = '四川省公共资源交易网'
        return item

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