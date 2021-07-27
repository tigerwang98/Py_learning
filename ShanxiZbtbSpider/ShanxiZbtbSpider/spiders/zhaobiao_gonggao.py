import scrapy

class ZhaobiaoGonggaoSpider(scrapy.Spider):
    name = 'zhaobiao_gonggao'
    allowed_domains = ['www.sxbid.com.cn']
    start_urls = ['http://www.sxbid.com.cn/f/list-6796f0c147374f85a50199b38ecb0af6.html',
                  'http://www.sxbid.com.cn/f/list-54f5e594f4314654aadf09f7c9ae28bf.html',
                  'http://www.sxbid.com.cn/f/list-0e02eed6a6714f82a729dcceadea02b0.html']
    start_pageNo = 1

    def parse_list(self, response):
        cur_pageNo = response.meta['pageNo']
        next_pageNo = cur_pageNo + 1
        cate_id = response.meta['cate_id']
        self.logger.info('当前是第%s页' % cur_pageNo)
        selector = scrapy.Selector(response)
        table = selector.xpath('//table[@class="download_table"]')[0]
        tr_list = table.xpath('.//tbody//tr')
        for tr in tr_list:
            title = tr.xpath('.//td[2]/@title').get()
            href = response.urljoin(tr.xpath('.//td[2]/a/@href').get())
            pubtime = tr.xpath('.//td[4]//text()').get()
            data = {'title': title, 'url': href, 'pubtime': pubtime, 'cate_id': cate_id}
            if 'loginFlag=loginAndPayAndTime' in href:
                print('当前数据需要登录！放弃！')
            else:
                yield scrapy.Request(url=href, meta=data, callback=self.parse_detail, priority=1)
        param = 'form_random_token=&pageNo=%s&pageSize=15&accordToLaw=1&resourceType=1&title=&publishTimeRange=' % next_pageNo
        if cur_pageNo < 5:
            meta = {'pageNo': next_pageNo, 'cate_id': cate_id}
            header = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            yield scrapy.Request(url=response.url, meta=meta, method='POST', headers=header, body=param, callback=self.parse_list, priority=0)


    def parse_detail(self, response):
        data = response.meta
        title = data['title']
        cate_id = data['cate_id']
        pubtime = data['pubtime']
        outurl = data['url']
        selector = scrapy.Selector(response)
        info = selector.xpath('//div[@class="page_main"]').get()
        item = {'area_id': 23, 'cate_id': cate_id, 'location': '山西省',
                'title': title, 'pubtime': pubtime, 'author': '山西省招标投标公共服务平台',
                'outurl': outurl, 'info': info}
        return item