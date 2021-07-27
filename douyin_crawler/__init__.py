# encoding: utf-8
"""
@project = temp
@file = __init__
@author= wanghu
@create_time = 2021/7/14 11:31
"""
import logging
import requests
from urllib.parse import quote,unquote
logging.getLogger().setLevel(logging.INFO)

base_url = 'https://www.douyin.com/aweme/v1/web/search/item/?'

def save_video(title, url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Referer': 'https://www.douyin.com/',
    }
    resp = requests.get(url=url, headers=header)
    with open(r'C:\\Users\\123\\Desktop\\%s.mp4' % title, 'wb') as f:
        logging.info('正在保存%s的视频...' % title)
        f.write(resp.content)

def get_list(keyword):
    list_url = base_url + 'device_platform=webapp&' \
                          'aid=6383&channel=channel_pc_web&search_channel=aweme_video_web&sort_type=0&' \
                          'publish_time=0&keyword=%s&search_source=normal_search&query_correct_type=1&' \
                          'is_filter_search=0&offset=0&count=24&version_code=160100&version_name=16.1.0&' \
                          'cookie_enabled=true&screen_width=1670&screen_height=940&browser_language=zh-CN&browser_platform=Win32&' \
                          'browser_name=Mozilla&browser_version=5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36&browser_online=true&'\
                          '_signature=_02B4Z6wo00f01G2GfEgAAIDD3XeQgjibvexthnjAAHuX1c'%(quote(keyword))
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'referer': 'https://www.douyin.com/search/%E5%92%8C%E4%BB%8E%E5%B0%8F%E4%B8%80%E8%B5%B7%E9%95%BF%E5%A4%A7%E7%9A%84%E5%A7%90%E5%A7%90%E8%B0%88%E6%81%8B%E7%88%B1?source=normal_search&aid=82f83a28-7d2c-43e1-ac77-6be64b4f12ef&enter_from=main_page'
    }


if __name__ == "__main__":
    pass