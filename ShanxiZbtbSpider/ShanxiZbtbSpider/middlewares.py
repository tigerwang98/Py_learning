# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import scrapy
import json
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from .settings import DEFAULT_REQUEST_HEADERS
from icecream import ic
class ShanxizbtbspiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.
        # Must return only requests (not items).
        for request_obj in start_requests:
            url = request_obj.url
            if 'list-6796f0c147374f85a50199b38ecb0af6' in url:
                cate_id = 1
            elif 'list-54f5e594f4314654aadf09f7c9ae28bf' in url:
                cate_id = 2
            else:
                cate_id = 3
            data = {'pageNo': spider.start_pageNo, 'cate_id': cate_id}
            param = {
                "form_random_token": "",
                "pageNo": data['pageNo'],
                "pageSize": "15",
                "accordToLaw": 1,
                "resourceType": 1,
                "title": "",
                "publishTimeRange": "",
            }
            resp = scrapy.Request(url=url, method='POST', meta=data, body=json.dumps(param), callback=spider.parse_list)
            yield resp

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ShanxizbtbspiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
         return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
