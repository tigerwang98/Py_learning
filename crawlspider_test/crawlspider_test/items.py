# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlspiderTestItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    pubtime = scrapy.Field()
    area_id = scrapy.Field()
    city_id = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    add_time = scrapy.Field()
    info = scrapy.Field()
    file_url = scrapy.Field()
