# -*- coding: utf-8 -*-
import scrapy
from dingxiangyuan import settings
from dingxiangyuan.items import DingxiangyuanItemLoader, BoardItem


def get_start_urls():
    urls = [url for url in settings.BOARD_MAP]
    return urls


class BoardSpider(scrapy.Spider):
    name = 'board'
    allowed_domains = ['dxy.cn']
    # start_urls = ['http://www.dxy.cn/bbs/board/112', 'http://neuro.dxy.cn/bbs/board/46']

    def start_requests(self):
        for url in get_start_urls():
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item_loader = DingxiangyuanItemLoader(item=BoardItem(), response=response)
        board_id = settings.BOARD_MAP[response.url][0]
        board_name = settings.BOARD_MAP[response.url][1]
        board_url = response.url
        item_loader.add_value("board_id", board_id)
        item_loader.add_value("board_name", board_name)
        item_loader.add_value("board_url", board_url)
        item_loader.add_xpath("topic_num", '//div[@id="board"]/div/div/span[3]/text()')
        item_loader.add_xpath("moderator_url_list", '//div[@id="moderator"]/ul/li[2]/div/ul/li/a/@href')
        board_item = item_loader.load_item()
        yield board_item

