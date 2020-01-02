# -*- coding: utf-8 -*-

# Scrapy settings for dingxiangyuan project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'dingxiangyuan'

SPIDER_MODULES = ['dingxiangyuan.spiders']
NEWSPIDER_MODULE = 'dingxiangyuan.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 8

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    # 'Cookie': 'DXY_USER_GROUP=51; __auc=9957195716ece6c57af7ceec4b8; _ga=GA1.2.479266354.1575421237; JUTE_BBS_DATA=3f5bf0c1bf2fff84c25a59217af4a9e1b9f282e015aaea25127b5e0a88c724f1e0638a52f14d12828250f0eae037175c9f77313c2128052ee380e4fbb415fd9a3c0236dd91ca7c609c7758bfb16c995c; ifVisitOldVerBBS=true; Hm_lvt_b360de795e616b36eea2a3f75665b3cb=1575593776; __utmz=1.1576488037.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); JUTE_SESSION_ID=2d0cd959-7b4f-4505-a555-77538d9345ae; JUTE_TOKEN=cd5287a4-581c-4263-ac97-2c7764da90b3; Hm_lvt_8a6dad3652ee53a288a11ca184581908=1577064672,1577066616,1577071063,1577071447; __utmc=1; dxy_da_cookie-id=1fe540844ff7085574ed4ee1a92b2aed1577071448165; __asc=94531df516f31b130b6a96b7813; __utma=1.1027796917.1577005341.1577070130.1577086694.4; CMSSESSIONID=9B4643CEFA01BFA4ACF5911631887D6B-n1; Hm_lpvt_8a6dad3652ee53a288a11ca184581908=1577087783; JUTE_SESSION=de49a1d18b5567c269ac72f3e12dbbacd4479aed1841cb936706a71a4dff3471e72c63b7ffc6c5b7c2f1b3e2a98af667d83029a314df602a4ceffbe5539b24c549348abdbfa4b6ee; __utmb=1.15.7.1577089092910',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'DXY_USER_GROUP=51; __auc=9957195716ece6c57af7ceec4b8; _ga=GA1.2.479266354.1575421237; JUTE_BBS_DATA=3f5bf0c1bf2fff84c25a59217af4a9e1b9f282e015aaea25127b5e0a88c724f1e0638a52f14d12828250f0eae037175c9f77313c2128052ee380e4fbb415fd9a3c0236dd91ca7c609c7758bfb16c995c; ifVisitOldVerBBS=true; Hm_lvt_b360de795e616b36eea2a3f75665b3cb=1575593776; __utmz=1.1576488037.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); JUTE_SESSION_ID=2d0cd959-7b4f-4505-a555-77538d9345ae; JUTE_TOKEN=cd5287a4-581c-4263-ac97-2c7764da90b3; Hm_lvt_8a6dad3652ee53a288a11ca184581908=1577064672,1577066616,1577071063,1577071447; __utmc=1; dxy_da_cookie-id=3538d158adc905cf68cb935a695d61c71577094662396; __asc=0b34c1a616f322ac98d865eaf24; CMSSESSIONID=AB7D866998ABE12DD956FDDBF6C7123C-n1; __utma=1.1027796917.1577005341.1577086694.1577094663.5; __utmt=1; __utmb=1.20.9.1577096717327; bannerData={"banner":false,"message":"不显示banner"}; Hm_lpvt_8a6dad3652ee53a288a11ca184581908=1577096727; JUTE_SESSION=a89ca7b004443cd64950da07a6c2b74bac08a4fe7d201fd83cef4f1b3c1053731e660f69f9ea739bd453e1169e487abf3e10a6d82d96ff43d311e3c88a5a0c1255e66799c38387c6',
    'Host': 'www.dxy.cn',
    'Upgrade-Insecure-Requests': 1,
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',

}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'dingxiangyuan.middlewares.DingxiangyuanSpiderMiddleware': 543,
# }

USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
#
# IPLIST = [
#     'https://115.28.209.249:3128',
#     'https://192.99.245.228:3128',
#     'https://219.223.251.173:3128',
#     'https://119.28.152.208:80',
#     'https://210.5.149.43:8090',
#     'https://114.251.228.124:3128',
# ]

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'dingxiangyuan.middlewares.DingxiangyuanDownloaderMiddleware': 543,
    'dingxiangyuan.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
# 'scrapy.extensions.telnet.TelnetConsole': None,
#  'dingxiangyuan.extensions.MyExtension': 200,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'dingxiangyuan.pipelines.PostgresSQLPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 1
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 10
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 5.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

LOG_LEVEL = 'WARNING'

REDIRECT_ENABLED = False

POSTGRESQL_HOST = "127.0.0.1"
POSTGRESQL_DATABASE = "dingxiangyuan"
POSTGRESQL_USER = "postgres"
POSTGRESQL_PASSWORD = "0000"
POSTGRESQL_PORT = "5432"

DATABASE_ENGINE = 'postgresql://postgres:0000@127.0.0.1:5432/dingxiangyuan'

BOARD_MAP = {
    'http://cardiovascular.dxy.cn/bbs/board/47': [1, '心血管'],  # 心脏病 脑血管
    'http://www.dxy.cn/bbs/board/87': [2, '肿瘤'],  # 恶性肿瘤
    'http://chest.dxy.cn/bbs/board/58': [3, '呼吸胸外'],  # 呼吸系统疾病
    'http://www.dxy.cn/bbs/board/112': [4, '急救与危重病'],  # 损伤和中毒
    'http://www.dxy.cn/bbs/board/92': [5, '内分泌'],  # 内分泌营养和代谢疾病
    'http://www.dxy.cn/bbs/board/188': [6, '消化内科'],   # 消化系统疾病
    'http://neuro.dxy.cn/bbs/board/46': [7, '神经系统'],  # 神经系统疾病
    'http:///bbs/board/49': [8, '肾脏泌尿'],  # 泌尿生殖系统
    'http://www.dxy.cn/bbs/board/146': [9, '感染'],  # 传染病
}

BOARD_ID_MAP = {
    1: ['心血管', 'http://cardiovascular.dxy.cn/bbs/board/47'],
    2: ['肿瘤医学', 'http://www.dxy.cn/bbs/board/87'],
    3: ['呼吸胸外', 'http://chest.dxy.cn/bbs/board/58'],
    4: ['危重急救', 'http://www.dxy.cn/bbs/board/112'],
    5: ['内分泌', 'http://www.dxy.cn/bbs/board/92'],
    6: ['消化内科', 'http://www.dxy.cn/bbs/board/188'],
    7: ['神经内外',  'http://neuro.dxy.cn/bbs/board/46'],
    8: ['肾脏泌尿', 'http://www.dxy.cn/bbs/board/49'],
    9: ['感染', 'http://www.dxy.cn/bbs/board/146'],
}


# MONGO_URI = 'mongodb://127.0.0.1:27017/'
# MONGO_DB = 'dingxiangyuan'

# #################################### scrapy实现redis缓存去重 ############################################
REDIS_HOST = '127.0.0.1'  # 主机名
REDIS_PORT = 6379  # 端口
# REDIS_PARAMS = {'password':'0000'}                 # Redis连接参数             默认：REDIS_PARAMS = {'socket_timeout': 30,'socket_connect_timeout': 30,'retry_on_timeout': True,'encoding': REDIS_ENCODING,}）
REDIS_ENCODING = "utf-8"

SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = 'dingxiangyuan.dupeFilter.RedisDupeFilter'
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'  # 默认使用优先级队列（默认），其他：PriorityQueue（有序集合），FifoQueue（列表）、LifoQueue（列表）
SCHEDULER_QUEUE_KEY = '%(spider)s:requests'  # 调度器中请求存放在redis中的key
SCHEDULER_SERIALIZER = "scrapy_redis.picklecompat"  # 对保存到redis中的数据进行序列化，默认使用pickle
SCHEDULER_PERSIST = True  # 是否在关闭时候保留原来的调度器和去重记录，True=保留，False=清空
SCHEDULER_FLUSH_ON_START = False  # 是否在开始之前清空 调度器和去重记录，True=清空，False=不清空
SCHEDULER_DUPEFILTER_KEY = '%(spider)s:dupefilter'  # 去重规则，在redis中保存时对应的key

from scrapy_redis.scheduler import Scheduler
