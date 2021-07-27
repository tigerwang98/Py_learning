# encoding: utf-8
"""
@project = temp
@file = uploadfile_test
@author= wanghu
@create_time = 2021/6/21 18:55
"""
import os
import requests
import sys


def processFile(fileurl, filename, **kwargs):
    assert isinstance(fileurl, str)
    assert isinstance(filename, str)
    upload_url = 'http://192.168.1.241:8061/group2/upload'
    temp_dir = r'../files/Temp/'
    # if isBigfile(fileurl, **kwargs):
    #     print('{} 大小超过30M!放弃下载~~~~~~'.format(filename))
    #     sys.exit(1)
    intro = ''
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    try:
        file = os.path.join(temp_dir, filename)
        r = requests.get(fileurl, stream=True, **kwargs)
        with open(file, 'wb') as s:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    s.write(chunk)
    except Exception as e:
        print('下载{0}失败!失败原因为: {1} 当前链接为{2}'.format(filename, str(e), fileurl))
        return
    with open(file, 'rb') as f:
        res = requests.post(upload_url, data={'output': 'json', 'path': '', 'scene': ''}, files={'file': f})
    if res:
        intro = res.json().get('url')
        print('{} 上传成功!'.format(filename))
        os.remove(file)
    return intro

def isBigfile(file_url, **kwargs):
        res = requests.head(file_url, **kwargs)
        if not res:
            return True
        content_lenth, content_type = res.headers.get('Content-Length', 0), res.headers.get('Content-Type', '')
        if not content_lenth:
            if file_url.split('.')[-1] not in ['rar', 'zip']:
                return False
            else:
                return True
        else:
            if all([content_lenth, int(content_lenth) <= (30 * 1024 * 1024), 'text' not in content_type]):
                return False
        return True

if __name__ == "__main__":
    # intro1 = processFile(filename='中电阳泉数字经济产业园（一期）项目 B1地块工程监理中标结果公示.pdf',fileurl='http://www.sxbid.com.cn/f/downloadByFileName?type=3&fname=2cd80d38-f02a-43b6-8835-5504443c9609')
    intro2 = processFile(filename='title.jpg', fileurl='http://115.231.208.175:6084/fileserver//down?md5=F8C51EB9B2CEA2F5871D5CE42781308F&bucket=2')
    # print('监理:', intro1)
    print(intro2)
