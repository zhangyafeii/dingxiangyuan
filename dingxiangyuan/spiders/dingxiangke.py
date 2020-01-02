# -*- coding: utf-8 -*-
from urllib.parse import unquote

import scrapy
from dingxiangyuan.items import DingxiangyuanItemLoader, DingXiangKeItem
from dingxiangyuan.DBHelper import redis_conn
import pandas as pd
from dingxiangyuan.DBHelper import db_conn


def get_start_urls():
    data1 = pd.read_sql(sql='select distinct author_url from posts_replies', con=db_conn)
    data2 = pd.read_sql(sql='select distinct user_url_unquote from dingxiangke', con=db_conn)
    start_urls = set(data1['author_url']) - set(data2['user_url_unquote'])
    if redis_conn.scard('dingxiangke_error_url') >= 1:
        error_urls = redis_conn.smembers('dingxiangke_error_url')
        error_urls = {unquote(url.decode()) for url in error_urls}
        start_urls = start_urls - error_urls
    return start_urls


class DingxiangkeSpider(scrapy.Spider):
    name = 'dingxiangke'
    allowed_domains = ['i.dxy.cn']
    # start_urls = ['http://i.dxy.cn/profile/yilulige', 'http://i.dxy.cn/profile/%E8%91%A3%E8%91%A3%E8%91%A3', 'http://i.dxy.cn/profile/%E5%8D%8E%E5%A4%8F%E8%A7%88%E9%9B%84', 'http://i.dxy.cn/profile/%E9%A1%BF%E9%9B%852019']
    # start_urls = ['http://i.dxy.cn/profile/%E8%91%A3%E8%91%A3%E8%91%A3', 'http://i.dxy.cn/profile/%E9%9B%B7%E6%96%87%E6%96%8C%E5%A4%A7%E5%A4%AB']
    start_urls = get_start_urls()

    # def start_requests(self):
        # start_urls = redis_conn.smembers('dingxiangke_start_urls')
        # if redis_conn.scard('dingxiangke_error_url') >= 1:
        #     error_urls = redis_conn.smembers('dingxiangke_error_url')
        #     error_urls = {url.decode() for url in error_urls}
        #     start_urls = start_urls - error_urls
        # for url in start_urls:
        #     yield scrapy.Request(url=url.decode(), callback=self.parse)

    def parse(self, response):
        item_loader = DingxiangyuanItemLoader(item=DingXiangKeItem(), response=response)
        item_loader.add_value('user_url', response.url)
        item_loader.add_value('user_url_unquote', unquote(response.url))
        item_loader.add_xpath('user_name', '//div[@class="banner-inner__user-id pa"]/a[1]/text()')
        item_loader.add_xpath('posts', '//ul[@class="main-nav-inner__nav-list fsb14 clearfix"]/li[3]/span[1]/text()')
        item_loader.add_xpath('distilled', '//ul[@class="main-nav-inner__nav-list fsb14 clearfix"]/li[4]/span[1]/text()')
        item_loader.add_xpath('score',  '//ul[@class="main-nav-inner__nav-list fsb14 clearfix"]/li[5]/span[1]/text()')
        item_loader.add_xpath('posts_voted', '//ul[@class="main-nav-inner__nav-list fsb14 clearfix"]/li[6]/span[1]/text()')
        item_loader.add_xpath('following', '//div[@class="follows-fans__items fl"][1]/p/a/text()')
        item_loader.add_xpath('follower', '//div[@class="follows-fans__items fl"][2]/p/a/text()')
        item_loader.add_xpath('dingdang', '//div[@class="follows-fans__items fl"][3]/p/a/text()')
        item_loader.add_xpath('user_level', 'string(//span[@class="level-wrap__level-title mr15"])')
        if response.xpath('//p[contains(@class, "details-wrap__items ")][1]/a'):
            item_loader.add_xpath('user_identify', 'string(//p[contains(@class, "details-wrap__items ")])')
        else:
            item_loader.add_value('user_identify', '未认证')
        if response.xpath('//div[@class="details-wrap color6"]/p[@class="details-wrap__items"]/text()'):
            item_loader.add_xpath('user_city', '//div[@class="details-wrap color6"]/p[@class="details-wrap__items"]/text()')
        else:
            item_loader.add_value('user_city', '未知')
        item_loader.add_xpath('posts_browsered', '//div[@class="statistics-wrap color6"]/ul/li[1]/p[2]/text()')
        item_loader.add_xpath('posts_faved', '//div[@class="statistics-wrap color6"]/ul/li[3]/p[2]/text()')
        item_loader.add_xpath('online_time', '//div[@class="statistics-wrap color6"]/ul/li[4]/p[2]/text()')
        dingxiangke_item = item_loader.load_item()
        yield dingxiangke_item


















