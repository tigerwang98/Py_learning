# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyFaguiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    pubtime = scrapy.Field()
    author = scrapy.Field()
    notify_code = scrapy.Field()
    area_id = scrapy.Field()
    city_id = scrapy.Field()
    url = scrapy.Field()
    add_time = scrapy.Field()
    info = scrapy.Field()
