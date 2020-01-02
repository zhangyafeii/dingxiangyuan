# -*- coding: utf-8 -*-
import scrapy
import re
import pandas as pd
from dingxiangyuan.items import DingxiangyuanItemLoader, TopicRateItem
from dingxiangyuan.DBHelper import db_conn


def get_start_urls():
    data1 = pd.read_sql(sql="select topic_url from posts_replies where floor=1", con=db_conn)
    data2 = pd.read_sql(sql="select topic_url from topic_rate_get", con=db_conn)
    topic_url = set(data1['topic_url']) - set(data2['topic_url'])
    return topic_url


class TopicRateSpider(scrapy.Spider):
    name = 'topic_rate'
    allowed_domains = ['www.dxy.cn', 'neuro.dxy.cn', 'chest.dxy.cn', 'cardiovascular.dxy.cn']
    # start_urls = ['http://chest.dxy.cn/bbs/topic/11838188']
    # start_urls = get_start_urls()

    def start_requests(self):
        print(get_start_urls())
        # for url in get_start_urls():
        #     yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item_loader = DingxiangyuanItemLoader(item=TopicRateItem(), response=response)
        topic_url = response.url
        rate_get = response.xpath('//div[@id="post_1"]//td[@class="tbc"]/div[1]/div[1]/ul//div[@class="rate-got"]/text()')
        rate_get = int(re.search(r'\d+', rate_get.extract_first()).group()) if rate_get else 0
        item_loader.add_value('rate_get', rate_get)
        topic_type = response.xpath('//div[@id="location"]/a[3]/text()')
        topic_type = topic_type.extract_first() if topic_type else '其它'
        board_name = response.xpath('//div[@id="board"]/div/h1/a/text()').extract_first()
        item_loader.add_value('topic_url', topic_url)
        item_loader.add_value('topic_type', topic_type)  # 主题帖类型
        item_loader.add_value('board_name', board_name)  # 所属板块
        topic_rate_item = item_loader.load_item()
        yield topic_rate_item

