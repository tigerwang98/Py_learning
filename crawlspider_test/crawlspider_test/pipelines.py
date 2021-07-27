# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from twisted.enterprise import adbapi
from time import time

class CrawlspiderTestPipeline:
    def __init__(self, mysql_config):
        self.db = adbapi.ConnectionPool(
            mysql_config['DRIVER'],
            host=mysql_config['HOST'],
            port=mysql_config['PORT'],
            user=mysql_config['USER'],
            password=mysql_config['PASSWORD'],
            db=mysql_config['DATABASE'],
            charset='utf8'
        )

    @classmethod
    def from_crawler(cls, crawler):
        mysql_config = crawler.settings['MYSQL_CONFIG']
        return cls(mysql_config)

    def process_item(self, item, spider):
        self.db.runInteraction(self.insert_item, item)
        return item

    def insert_item(self, cursor, item):
        sql = '''INSERT INTO `scrapy_test`(id, title, author, pubtime, outurl, fileurl, content, addtime) VALUES(null, %s, %s, %s, %s, %s,%s, %s) '''
        args = (item['title'], item['author'], item['pubtime'], item['outurl'], item['fileurl'], item['content'], int(time()))
        cursor.execute(sql, args)