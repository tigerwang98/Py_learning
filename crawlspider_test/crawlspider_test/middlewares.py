# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from .settings import *
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import base64
import sys
import random

PY3 = sys.version_info[0] >= 3


def base64ify(bytes_or_str):
    if PY3 and isinstance(bytes_or_str, str):
        input_bytes = bytes_or_str.encode('utf8')
    else:
        input_bytes = bytes_or_str

    output_bytes = base64.urlsafe_b64encode(input_bytes)
    if PY3:
        return output_bytes.decode('ascii')
    else:
        return output_bytes


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        # 代理服务器(产品官网 www.16yun.cn)
        proxyHost = "u5694.20.tp.16yun.cn"
        proxyPort = "6447"

        # 代理验证信息
        proxyUser = "16NPHKSJ"
        proxyPass = "287149"

        request.meta['proxy'] = "http://{0}:{1}".format(proxyHost, proxyPort)

        # 添加验证头
        encoded_user_pass = base64ify(proxyUser + ":" + proxyPass)
        request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass

        # 设置IP切换头(根据需求)
        tunnel = random.randint(1, 10000)
        request.headers['Proxy-Tunnel'] = str(tunnel)