# Scrapy settings for Scrapy_zixun project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Scrapy_zixun'

SPIDER_MODULES = ['Scrapy_zixun.spiders']
NEWSPIDER_MODULE = 'Scrapy_zixun.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Scrapy_zixun (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
# DOWNLOAD_TIMEOUT = 10
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 32
CONCURRENT_REQUESTS_PER_IP = 32

# Disable cookies (enabled by default)
COOKIES_ENABLED = False
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Scrapy_zixun.middlewares.ScrapyZixunSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'Scrapy_zixun.middlewares.ProxyMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'Scrapy_zixun.pipelines.ScrapyZixunPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# Redis相关配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PARAMS = {'db': 7}
# 调度器选择
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 去重规则对应处理的类
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
# 是否持久化，为false的话Redis关闭了 Redis数据也会被清空
SCHEDULER_PERSIST = True
# 代理配置
proxy_host = "u5694.20.tp.16yun.cn"
proxy_port = "6447"
proxy_user = "16NPHKSJ"
proxy_pass = "287149"
# 数据库配置
MYSQL_CONFIG = {
    'DRIVER': 'pymysql',
    'HOST': '127.0.0.1',
    'PORT': 3306,
    'DATABASE': 'test',
    'USER': 'root',
    'PASSWORD': '123456'
}
# 日志文件配置
LOG_LEVEL = 'DEBUG'
from .start_main import spider_name
LOG_FILE = r'C:\\Users\\123\\Desktop\\Scrapy_zixun\\log\\%s.log' % spider_name