# encoding: utf-8
"""
@project = Py_learing
@file = main
@author= wanghu
@create_time = 2021/8/25 17:25
"""
from WechatPub.insert_items import Items
from WechatPub.publicArticle import WeixinPub

if __name__ == '__main__':
    db = Items()
    crawler = WeixinPub()
    datas = crawler.run()
    while True:
        try:
            data = next(datas)
            if data:
                db.insertItem(data)
        except StopIteration:
            break
    db.close()
    crawler.close()