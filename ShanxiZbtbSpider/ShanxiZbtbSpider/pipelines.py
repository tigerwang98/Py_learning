# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .settings import MYSQL_CONFIG
from twisted.enterprise import adbapi
from time import time

class ShanxizbtbspiderPipeline:
    def __init__(self, ):
        self.db = adbapi.ConnectionPool(
            MYSQL_CONFIG['DRIVER'],
            host=MYSQL_CONFIG['HOST'],
            port=MYSQL_CONFIG['PORT'],
            user=MYSQL_CONFIG['USER'],
            password=MYSQL_CONFIG['PASSWORD'],
            db=MYSQL_CONFIG['DATABASE'],
            charset='utf8'
        )

    def process_item(self, item, spider):
        self.db.runInteraction(self.insert_item, item)
        return item

    def insert_item(self, cursor, item):
        sql = '''INSERT INTO `stang_bid_new`(id, area_id, cate_id, title, author, pubtime, outurl, location, info, add_time) VALUES(null, %s, %s, %s, %s, %s,%s, %s, %s, %s) '''
        args = (item['area_id'], item['cate_id'], item['title'], item['author'], item['pubtime'], item['outurl'], item['location'], item['info'], int(time()))
        cursor.execute(sql, args)