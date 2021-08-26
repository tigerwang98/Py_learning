# encoding: utf-8
"""
@project = Py_learing
@file = main
@author= wanghu
@create_time = 2021/8/25 17:25
"""
from WechatPub.insert_items import Items
from WechatPub.publicArticle import WeixinPub
import logging,copy
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    db = Items()
    crawler = WeixinPub()
    datas = crawler.run()
    while True:
        try:
            data = next(datas)
            if data:
                print_data = copy.deepcopy(data)
                print_data.pop('info')
                logging.info('consumer:%s' % print_data)
                db.insertItem(data)
        except StopIteration:
            break
    db.close()
    crawler.close()