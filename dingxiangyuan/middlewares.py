# -*- coding: utf-8 -*-

import logging
import os
import time

from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.request import request_fingerprint
from scrapy.utils.project import get_project_settings
from dingxiangyuan.DBHelper import redis_conn
from dingxiangyuan.settings import USER_AGENT_LIST
import random
from psycopg2 import errors

settings = get_project_settings()


class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = random.choice(USER_AGENT_LIST)
        if ua:
            request.headers.setdefault('User-Agent', ua)


class RandomProxy(object):
    def __init__(self, iplist):
        self.iplist = iplist

    @classmethod
    def from_crawler(cls, crawler):
        # 在settings中加载IPLIST的值
        return cls(
            iplist=crawler.settings.getlist('IPLIST')
        )

    def process_request(self, request, spider):
        # 在请求上添加代理
        proxy = random.choice(self.iplist)
        request.meta['proxy'] = proxy


class DingxiangyuanSpiderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DingxiangyuanDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        self.conn = redis_conn
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        if response.status != 200:
            if response.status == 503:
                time.sleep(1)
                return request
            else:
                self.conn.sadd(f'{spider.name}_error_url', request.url)
                self.logger.warning(f"{request.url, response.status} 该请求返回页面不正确, 忽略请求")
                raise IgnoreRequest()
        elif not self.judge_request_response(response, spider):
            with open('1.html', mode='w', encoding='utf-8') as f:
                f.write(response.text)
            self.logger.warning(f"{request.url, response.status} 该请求返回页面不正确, 忽略请求")
            time.sleep(1)
            raise IgnoreRequest()
        else:
            fd = request_fingerprint(request=request)
            self.conn.sadd(settings["SCHEDULER_DUPEFILTER_KEY"] % {'spider': spider.name}, fd)
            return response

    def judge_request_response(self, response, spider):
        """ 判断返回页面是否正确：是否可以取到需要的数据信息 """
        if spider.name == 'topics' and not response.xpath('//tr[contains(@class, "hoverClass")]'):
            return False
        if spider.name == 'posts_replies' and (not response.xpath('//div[@class="user-info"]') or not response.xpath('//div[starts-with(@id, "post_")]')):
            # spider.crawler.engine.close_spider(self, "cookie失效关闭爬虫")
            print('cookie失效，请输入验证码')
            time.sleep(1)
            return False
        if spider.name == 'dingxiangke' and not response.xpath('//div[@class="banner-inner__user-id pa"]/a[1]/text()'):
            return False
        if spider.name == 'topic_rate' and not response.xpath('//div[@id="post_1"]'):
            return False
        return True

    def process_exception(self, request, exception, spider):
        print(request.url, exception)

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
