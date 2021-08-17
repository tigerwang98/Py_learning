# encoding: utf-8
"""
@project = temp
@file = update_database
@author= wanghu
@create_time = 2021/7/15 9:35
"""

import pymysql

conn = pymysql.connect(host='192.168.1.252', user='root', password='123asd123asd', database='suitang', charset='utf8')
cur = conn.cursor()
# sql = '''delete from `stang_winning_prize` where prize_id=-1 and projectNmae="国际创新药械交流转换中心(国际创新药械交流转换中心)工程在春节期间不停工且假期期间农民工实名制系统上考勤日均人数超过50人，被海南省通报表扬，诚信加3分"'''
sql ='''INSERT INTO `stang_winning_prize`(`id`, `prizecode`, `projectNmae`, `joinCompany`, `joinPerson`, `getTime`, `nature`, `recomCompany`, `type`, `company_id`, `awarding_agency`, `prize_level`, `prize_id`, `url`, `area_id`, `city_id`, `pic_url`) VALUES (760469, '', '国际创新药械交流转换中心(国际创新药械交流转换中心)工程在春节期间不停工且假期期间农民工实名制系统上考勤日均人数超过50人，被海南省通报表扬，诚信加3分', '中能建（海南）有限公司\n', '', '2021-04-15', '', '', '企业荣誉', 1441680, '海口市建筑业协会', '国家级', -1, '', 0, 0, '');'''
cur.execute(sql)
conn.commit()
cur.close()
conn.close()