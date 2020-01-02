## 丁香园
- 获取时间2019-12-13 - 2019-12-25

### 一、项目结构
```python
(dingxiangyuan-YzSOQweE) E:\ZhangYafei\project\丁香园\dingxiangyuan>tree /f
文件夹 PATH 列表
卷序列号为 9475-0EA0
E:.
│  main.py
│  Pipfile
│  Pipfile.lock
│  README.md
│  redis_test.py
│  requirements.txt
│  scrapy.cfg
│
├─dingxiangyuan
│  │  DBHelper.py
│  │  dupeFilter.py
│  │  extensions.py
│  │  items.py
│  │  middlewares.py
│  │  pipelines.py
│  │  settings.py
│  │  __init__.py
│  │
│  └─spiders
│          board.py
│          dingxiangke.py
│          posts_replies.py
│          topics.py
│          topic_rate.py
│          __init__.py
│
├─images
│      pipenvv shell.png
│
└─SQL_data
        board.sql
        dingxiangke.sql
        posts_replies.sql
        topics.sql
        topic_rate_get.sql
```

### 二、数据表准备
> - 板块信息表  
> - 主题帖表   
> - 帖子评论表  
> - 帖子积分表
> - 丁香客
> sql 文件在SQL_data目录下，在postgressql中新建五张表

### 三、启动项目
> 1. 进入虚拟环境
![shell](images/pipenvv%20shell.png)
> 2. 修改settings
> 板块信息配置
```python
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
```
> - 数据库的配置
```python
POSTGRESQL_HOST = "127.0.0.1"
POSTGRESQL_DATABASE = "dingxiangyuan"
POSTGRESQL_USER = "postgres"
POSTGRESQL_PASSWORD = "0000"
POSTGRESQL_PORT = "5432"

DATABASE_ENGINE = 'postgresql://postgres:0000@127.0.0.1:5432/dingxiangyuan'
```
> - scrapy-redis的配置
```python
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
```
> - PIPLINES
```python
ITEM_PIPELINES = {
    'dingxiangyuan.pipelines.PostgresSQLPipeline': 300,
}
```
> - MIDDLEWARES
```python
DOWNLOADER_MIDDLEWARES = {
    'dingxiangyuan.middlewares.DingxiangyuanDownloaderMiddleware': 543,
    'dingxiangyuan.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}
```
> 其它一些配置：headers和cookie

> - 3. 项目运行命令
> 进入项目目录,运行main.py文件,或者执行
```python
scrapy crawl spider_name   # 爬虫名称 team|charmer|posts|comments|users
```

