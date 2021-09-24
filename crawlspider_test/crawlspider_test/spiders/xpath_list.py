# encoding: utf-8
"""
@project = Py_learing
@file = xpath_list
@author= wanghu
@create_time = 2021/9/22 17:46
"""
info_xpath_list = [
    '//div[@class="xl_cont"]//div[@class="TRS_Editor"]',
    '//div[@class="xl_cont"]//div[@class="Custom_UnionStyle"]',
    '//div[@class="content"]',
    '//div[@class="gknbxq_detail"]',
    '//div[@class="content"]',
]
title_xpath_list = [
    '//div[@class="xl_cont"]//h3',
    '//h1[@class="f24 fontB fontWr blue"]//text()',
    '//strong[@id="ctl00_ContentPlaceHolder1_title"]//text()',
    '//div[@id="info_title"]//text()',
    '//div[@class="gknbxq_top"]/h2//text()',
    '//h1[@class="f26 fontWr"]//text()',
    '//h1[@class="f24 fontB blue fontWr"]//text()',
    '//h1[@class="f24"]//text()',
    '//div[@class="title"]//text()',

]
pubtime_xpath_list = [
    '//div[@class="xl_cont"]//div[@class="time"]//div[@class="fr"]//text()',
    '//div[@class="xl_cont"]//div[@class="xl_table"]/table//tr[2]//td[4]//text()',
    '//div[@class="time"]//div[2]//text()',
    '//div[@class="gknbxq_top"]/p//text()',
    '//div[@class="date"]/span//text()',
    '//div[@id="info_source"]//p//text()',
    '//div[@class="time"]//text()',
    '//div[contains(@class, "time f12")]//text()',
    '//div[@class="fl"]//text()',
]
xpath_dict = {
    'pub_time': pubtime_xpath_list,
    'title': title_xpath_list,
    'infos': info_xpath_list,
}