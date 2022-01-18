# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from twisted.enterprise import adbapi
import time

class ScrapyFaguiPipeline:
    def __init__(self, mysql_config):
        self.db = adbapi.ConnectionPool(
            mysql_config['DRIVER'],
            host=mysql_config['HOST'],
            port=mysql_config['PORT'],
            user=mysql_config['USER'],
            password=mysql_config['PASSWORD'],
            db=mysql_config['DATABASE'],
            charset='utf8',
            cp_max=10,
            cp_reconnect=True,
        )

    @classmethod
    def from_crawler(cls, crawler):
        mysql_config = crawler.settings['MYSQL_CONFIG']
        return cls(mysql_config)

    def process_item(self, item, spider):
        self.db.runInteraction(self.insert_item, item)
        return item

    def insert_item(self, cursor, item):
        infos = self.addslashes(item['info'])
        sql_zixun = '''INSERT INTO `stang_zixun`(title, pubtime, author, area_id, city_id, url, addtime) VALUES(%s, %s, %s, %s, %s, %s, %s) '''
        # sql_zixun_file = '''INSERT INTO `stang_zixun_file`(forid, file_url) VALUES(%s, %s)'''
        sql_zixun_info = '''INSERT INTO `stang_zixun_info`(forid, info) VALUES(%s, %s)'''
        args = (
            item['title'], item['pubtime'], item['author'], item['area_id'], item['city_id'], item['url'], int(time.time()))
        cursor.execute(sql_zixun, args)
        forid = cursor.lastrowid
        cursor.execute(sql_zixun_info, (forid, infos))

    def addslashes(self, s):
        l = ["\\", '"', "'", "\0", ]
        for i in l:
            if i in s:
                s = s.replace(i, '\\' + i)
        return s