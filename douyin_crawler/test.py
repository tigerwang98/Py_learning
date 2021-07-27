# encoding: utf-8
"""
@project = temp
@file = test
@author= wanghu
@create_time = 2021/7/14 17:05
"""
import time
import requests
from urllib.parse import urlencode, urljoin

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
    'referer': 'https://www.douyin.com/user/MS4wLjABAAAAgq8cb7cn9ByhZbmx-XQDdRTvFzmJeBBXOUO4QflP96M?enter_method=video_title&author_id=66598046050&group_id=6976510986547105060&log_pb=%7B%22impr_id%22%3A%22021624413357501fdbddc0100fff0020a9b342d0000001b0ac6ec%22%7D&enter_from=video_detail',
}
session = requests.session()
session.headers = headers
# session.get('https://www.douyin.com') # 部分请求可能需要cookie，如获取用户喜欢列表，加一步获取cookie即可
url = "https://www.douyin.com/aweme/v1/web/aweme/post/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=MS4wLjABAAAAgq8cb7cn9ByhZbmx-XQDdRTvFzmJeBBXOUO4QflP96M&max_cursor=1623331736000&count=10&publish_video_strategy_type=2&version_code=160100&version_name=16.1.0"

data = {
    "method":"get",
    "url":url
}
resp = requests.post('http://59.110.158.68:8787/sign', data=data).json()
if resp['error_code'] == 0:
    _signature = resp['result']['_signature']
    print(resp)
    print(_signature)
    print('*'*50)
    url += "&" + urlencode({"_signature":_signature})
    response = session.get(url)
    print(response.json())
