# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShanxizbtbspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    area_id = scrapy.Field()
    cate_id = scrapy.Field()
    location = scrapy.Field()
    title = scrapy.Field()
    pubtime = scrapy.Field()
    author = scrapy.Field()
    outurl = scrapy.Field()
    info = scrapy.Field()
