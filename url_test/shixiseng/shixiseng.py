# encoding: utf-8
"""
@project = temp
@file = shixiseng
@author= wanghu
@create_time = 2021/7/26 14:22
"""
import time

import requests
import re
from lxml import etree
from fontTools.ttLib import TTFont
import io
import base64

class ShixisengSpider():
    def __init__(self, file_path):
        self.baseMap = {
            '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
            '10': '一', '11': '师', '12': 'X', '13': '会', '14': '四', '15': '计', '16': '财',
            '17': '场', '18': 'D', '19': 'H', '20': 'L', '21': 'P', '22': 'T', '23': '聘',
            '24': '招', '25': '工', '26': 'd', '27': '周', '28': 'l', '29': '端', '30': 'p',
            '31': '年', '32': 'h', '33': 'x', '34': '设', '35': '程', '36': '二', '37': '五',
            '38': '天', '39': 't', '40': 'C', '41': 'G', '42': '前', '43': 'K', '44': 'O', '45': '网',
            '46': 'S', '47': 'W', '48': 'c', '49': 'g', '50': 'k', '51': 'o', '52': 's', '53': 'w',
            '54': '广', '55': '市', '56': '月', '57': '个', '58': 'B', '59': 'F', '60': '告', '61': 'N',
            '62': 'R', '63': 'V', '64': 'Z', '65': '作', '66': 'b', '67': 'f', '68': 'j', '69': 'n',
            '70': 'r', '71': 'v', '72': 'z', '73': '三', '74': '互', '75': '生', '76': '人', '77': '政',
            '78': 'A', '79': 'J', '80': 'E', '81': 'I', '82': '件', '83': 'M', '84': '行', '85': 'Q',
            '86': 'U', '87': 'Y', '88': 'a', '89': 'e', '90': 'i', '91': 'm', '92': '软', '93': 'q',
            '94': 'u', '95': '银', '96': 'y', '97': '联'
        }
        self.font = self.save_ttfORxml(file_path)
        self.glyphMap = self.generate_alphaTable()

    def save_ttfORxml(self, path):
        with open(path, 'rb') as f:
            font_face = f.read()
        font = TTFont(io.BytesIO(font_face))
        TTFont.saveXML(font, './font.xml')
        TTFont.save(font, './font.ttf')
        return font

    def generate_alphaTable(self):
        glyphNameMap = self.font.getGlyphOrder()
        glyphMap = {}
        for glyphID, name in enumerate(glyphNameMap[2:]):
            glyphMap[name] = str(glyphID)
        return glyphMap

    def parse_font(self, html_info):
        handled_info = re.sub(r'&#x|#x', '0x', html_info)
        codeNameMap = self.font.getBestCmap()
        for code, name in codeNameMap.items():
            if name in self.glyphMap.keys():
                final_font = self.baseMap[self.glyphMap[name]]
            elif name == 'x':
                continue
            else:
                final_font = self.baseMap[name]
            handled_info = handled_info.replace(hex(code), final_font)
        return handled_info

    def send_request(self, page):
            request_url = f'https://www.shixiseng.com/interns?page={page}&type=intern&keyword=%E4%BA%92%E8%81%94%E7%BD%91%2FIT&area=&months=&days=&degree=&official=&enterprise=&salary=-0&publishTime=&sortType=&city=%E6%88%90%E9%83%BD&internExtend='
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            }
            ret = requests.post(url=request_url, headers=header)
            if ret.status_code == 200:
                return ret.text

    def parse_web_info(self, info):
        html_info = self.parse_font(info)
        html = etree.HTML(html_info.replace('&amp;', ''))
        for div in html.xpath('//div[contains(@class, "intern-wrap")]/div[contains(@class, "intern-detail")]'):
            job_div = div.xpath('.//div[contains(@class, "intern-detail__job")]')[0]
            job_name = job_div.xpath('./p[1]/a/@title')[0]
            money = job_div.xpath('./p[1]/span/text()')[0]
            detail_url = job_div.xpath('./p[1]/a/@href')[0]
            job_city = job_div.xpath('./p[2]/span[1]/text()')[0]
            work_time = job_div.xpath('./p[2]/span[3]/text()')[0]
            deadline = job_div.xpath('./p[2]/span[5]/text()')[0]

            company_div = div.xpath('.//div[contains(@class, "intern-detail__company")]')[0]
            company_name = company_div.xpath('./p[1]/a/@title')[0]
            company_category = company_div.xpath('./p[2]/span[1]/text()')[0]
            company_scale = company_div.xpath('./p[2]/span[3]/text()')[0]


            print('=================招 聘 需 求====================')
            print('工作名称：%s  薪资：%s  上班时间：%s  实习期限：%s  工作地点：%s' % (job_name, money, work_time, deadline, job_city))
            print('公司名称：%s  所属行业：%s  公司规模：%s' % (company_name, company_category, company_scale))
            print('详情链接：%s' % detail_url)
            print('================================================')

    def run(self):
        for page in range(1, 5):
            response = self.send_request(page)
            self.parse_web_info(response)

if __name__ == '__main__':
    spider = ShixisengSpider(file_path=r'./font_face')
    spider.run()