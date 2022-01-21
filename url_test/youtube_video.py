# encoding: utf-8
"""
@project = Py_learing
@file = youtube_video
@author= wanghu
@create_time = 2022/1/10 9:42
"""
import re
import os
import time
import requests
from lxml import etree
import json

proxy = {
    'http': '127.0.0.1:10809',
    'https': '127.0.0.1:10809',
}
header = {
    'Referer': 'https://www.youtube.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
}

def find_video_script(url):
    res = requests.get(url=url, headers=header, proxies=proxy)
    print('请求成功！')
    if res.status_code == 200:
        html = etree.HTML(res.text)
        for scripts in html.xpath('//body//script'):
            script = etree.tostring(scripts, encoding='utf-8').decode()
            # print(script)
            if 'ytInitialPlayerResponse' in script:
                try:
                    json_data = re.search(r'var ytInitialPlayerResponse =.*var ', script).group()
                except:
                    print('解析失败！请检查请求是否正确！')
                    raise BaseException
                return re.sub(r'var|ytInitialPlayerResponse', '', json_data)[:-2].strip()

def parse_script(script):
    print(re.sub(r'=', '', script, count=1).strip())
    script = json.loads(re.sub(r'=', '', script, count=1).strip())
    for data in script['streamingData']['adaptiveFormats']:
        if 'mp4' in data['mimeType']:
            download_url = data['url']
            video_title = script['microformat']['playerMicroformatRenderer']['title']['simpleText']
            try:
                description = script['microformat']['playerMicroformatRenderer']['description']['simpleText']
            except KeyError:
                description = ''
            video_author = script['videoDetails']['author']
            video_length = script['microformat']['playerMicroformatRenderer']['lengthSeconds']
            video_category = script['microformat']['playerMicroformatRenderer']['category']
            video_watches = script['microformat']['playerMicroformatRenderer']['viewCount']
            video_publishdate = script['microformat']['playerMicroformatRenderer']['publishDate']
            video_uploaddate = script['microformat']['playerMicroformatRenderer']['uploadDate']
            item = {'video_title': video_title, 'description': description, 'video_author': video_author,
                    'video_length': video_length, 'video_category': video_category, 'video_watches': video_watches,
                    'video_publishdate': video_publishdate, 'video_uploaddate': video_uploaddate, 'download_url': download_url}
            print('item:', item)
            return item
    return {}

def video_insert(item, save_path):
    author = item['video_author']
    title = item['video_title']
    url = item['download_url']
    list_file_path = os.path.join(save_path, author)
    if not os.path.exists(list_file_path):
        os.mkdir(list_file_path)
    detail_file_path = os.path.join(list_file_path, title)
    if not os.path.exists(detail_file_path):
        os.mkdir(detail_file_path)
    file_path = detail_file_path + '\\' + title +'.mp4'
    download(url, file_path)

def download(download_url, save_path):
    print('正在下载中... ...')
    total_size = Initial_jindutiao(download_url)
    res = requests.get(download_url, headers=header, proxies=proxy, stream=True)
    count = 0
    with open(save_path, 'wb') as f:
        for chunk in res.iter_content(chunk_size=4096):
            echo_download_process(total_size, count)
            count += 1
            if chunk:
                f.write(chunk)
    print('下载完成!')

def Initial_jindutiao(download_url):
    while True:
        res = requests.head(download_url, headers=header, proxies=proxy)
        total_size = int(res.headers['Content-Length'])
        if total_size > 0:
            return total_size
        print('获取视频失败！正在重试中... ...')

def echo_download_process(total_size, download_count):
    size = 100
    total_size = int(total_size)
    jindutiao = int(download_count * 4096 * size / total_size)
    print('\r', '>' * jindutiao, '=' * (size-jindutiao), '  ', '{}%'.format(jindutiao), end='', flush=True, sep='')


if __name__ == '__main__':
    url = 'https://www.youtube.com/watch?v=h_pj59N_6ro'
    save_path = r'C:\\Users\\123\\Desktop\\Namewee'
    script = find_video_script(url=url)
    item = parse_script(script)
    if item:
        video_insert(save_path, item)
