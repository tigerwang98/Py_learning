from os.path import dirname
import os

# 数据库配置
MYSQL_SERVER = '47.108.238.165'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'asdzxc123'
MYSQL_DB = 'test'

# redis配置
REDIS_SERVER = '47.108.238.165'
REDIS_port = 6379
REDIS_USER = ''
REDIS_PASSWORD = 'asdzxc123'
REDIS_DB = 0

BASE_FILE_PATH = os.path.join(dirname(os.path.abspath(r'..')), 'files')