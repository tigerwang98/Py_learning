import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from gne import GeneralNewsExtractor
from ..items import CrawlspiderTestItem
from dateparser import parse
import re

class TestSpider(CrawlSpider):
    name = 'test'
    allowed_domains = ['newssc.org',]
    start_urls = ['http://www.newssc.org/']
    domain = [
        r'http://scnews.newssc.org/system/\d+/\d+\.html',
        r'http://china.newssc.org/system/\d+/\d+\.html',
        r'http://world.newssc.org/system/\d+/\d+\.html',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'http://\w+\.newssc.org/system/\d+/\d+\.html'), callback='parse_detail', follow=True),
        # Rule(LinkExtractor(allow=domain[1]), callback='parse_detail', follow=True),
        # Rule(LinkExtractor(allow=domain[2]), callback='parse_detail', follow=True),
    )

    def get_standard_pubtime(self, pub_time):
        if not isinstance(pub_time, str):
            return TypeError
        if pub_time.strip() == '-':
            return '-'
        pub_time = re.sub(r'\\r|\\n|\\t', '', pub_time)
        pubtime = parse(pub_time)
        if pubtime:
            return str(pubtime).split(' ')[0]
        else:
            self.logger.info('%s 时间格式不对！' % pub_time)
            return TypeError

    def parse_detail(self, response):
        gen_extractor = GeneralNewsExtractor()
        result = gen_extractor.extract(response.text)
        title = result['title']
        author = result['author']
        pubtime = self.get_standard_pubtime(result['publish_time'])
        content = result['content']
        file_url = ",".join(result['images'])
        outurl = response.url
        item = CrawlspiderTestItem(title=title, author=author, pubtime=pubtime, content=content, fileurl=file_url, outurl=outurl)
        return item
