# encoding: utf-8
"""
@project = Py_learing
@file = main
@author= wanghu
@create_time = 2021/8/25 17:25
"""
import sys
from WechatPub.insert_items import Items
from WechatPub.publicArticle import WeixinPub
import logging,copy
from WechatPub.CONFIG import *
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    db = Items()
    crawler = WeixinPub()
    logging.info('开始读取作者列表... ...')
    with open(URL_CONFIG, 'r', encoding='utf-8') as f:
        authors = f.readlines()
    logging.info('作者列表读取成功！')
    for author in authors:
        author = author.strip('\n')
        for pg in range(PAGE):
            datas = crawler.run(author.strip('\n'), pg)
            for data in datas:
                print_data = copy.deepcopy(data)
                print_data.pop('info')
                logging.info('consumer:%s' % print_data)
                try:
                    db.insertItem(data)
                except Exception as e:
                    print(e)
                    print(data['title'])
                    with open('temp.html', 'w', encoding='utf-8') as f:
                        f.write(str(data['info']))