# -*- coding: utf-8 -*-
import scrapy
from dingxiangyuan.items import DingxiangyuanItemLoader, PostsRepliesItem
from dingxiangyuan.DBHelper import db_conn, redis_conn
import pandas as pd
from dingxiangyuan.settings import BOARD_ID_MAP


def get_topic_left_start_urls(board_id):
    board_name = BOARD_ID_MAP[board_id][0]
    topic_urls = pd.read_sql(sql="select distinct topic_url from posts_replies where board_name=%s", params=(board_name,), con=db_conn)
    topic_urls_floor_one = pd.read_sql(sql="select topic_url from posts_replies where floor=1 and board_name=%s", params=(board_name,), con=db_conn)
    has_topic_urls = set(topic_urls['topic_url']) - set(topic_urls_floor_one['topic_url'])
    topic_page_urls = redis_conn.smembers('topic_page_urls')
    start_urls = {url.decode() for url in topic_page_urls if url.decode().split('?')[0] in has_topic_urls}
    return start_urls


class PostsRepliesSpider(scrapy.Spider):
    name = 'posts_replies'
    allowed_domains = ['www.dxy.cn', 'neuro.dxy.cn', 'chest.dxy.cn', 'cardiovascular.dxy.cn']
    # start_urls = ['http://chest.dxy.cn/bbs/topic/37978225']
    # start_urls = ['http://chest.dxy.cn/bbs/topic/11838188']
    start_urls = get_topic_left_start_urls(board_id=9)

    @staticmethod
    def get_start_urls(board_id):
        data = pd.read_sql(sql="topics", con=db_conn, columns=["board_id", "topic_url"])
        topic_urls = set(data.loc[data.board_id == board_id, 'topic_url'])
        topic_page_urls = redis_conn.smembers('topic_page_urls')
        topic_urls = {url.decode() for url in topic_page_urls if url.decode().split('?')[0] in topic_urls}
        error_urls = redis_conn.smembers('posts_replies_error_url')
        error_urls = {url.decode() for url in error_urls}
        return topic_urls - error_urls

    # def start_requests(self):
    #     for url in self.get_start_urls(board_id=9):
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        topic_url = response.url.rsplit('?', maxsplit=1)[0]
        topic_type = response.xpath('//div[@id="location"]/a[3]/text()')
        topic_type = topic_type.extract_first() if topic_type else '其它'
        board_name = response.xpath('//div[@id="board"]/div/h1/a/text()').extract_first()
        topic_title = self.strings_prosses(
            response.xpath('//*[@id="postview"]/table/tbody/tr/th/h1/text()').extract_first())
        post_good_list = response.xpath('//div[@id="post_good"]/div[@class="good_post"]/table/tbody/tr')
        if post_good_list:
            for good_div in post_good_list:
                item_loader = DingxiangyuanItemLoader(item=PostsRepliesItem(), selector=good_div)
                item_loader.add_value('topic_url', topic_url)
                if good_div.xpath('td[@class="tbc"]/div[1]/div[1]/ul/div[@class="blt-icon lfloat"]'):
                    item_loader.add_value('hot', 1)
                else:
                    item_loader.add_value('hot', 0)
                floor = int(good_div.xpath(
                    'td[@class="tbc"]/div[1]/div[1]/ul/li/span[@class="layer"]/text()').extract_first().strip('楼'))
                item_loader.add_value('floor', floor)
                item_loader.add_value('topic_title', topic_title)
                if floor == 1:
                    item_loader.add_value('isTopic', 1)
                    item_loader.add_xpath('browser_num',
                                          'td[@class="tbc"]/div[@class="conbox"]//div[@class="post-info"]/span[last()-1]/text()')
                    item_loader.add_xpath('reply_num',
                                          'td[@class="tbc"]/div[@class="conbox"]//div[@class="post-info"]/span[last()]/text()')
                else:
                    item_loader.add_value('isTopic', 0)
                    item_loader.add_value('browser_num', 0)
                    item_loader.add_value('reply_num', 0)
                item_loader.add_xpath('content', 'string(td[@class="tbc"]/div[@class="conbox"]//td[@class="postbody"])')
                item_loader.add_value('topic_type', topic_type)  # 主题帖类型
                item_loader.add_value('board_name', board_name)  # 所属板块
                item_loader.add_xpath('post_time',
                                      'td[@class="tbc"]/div[@class="conbox"]//div[@class="post-info"]/span[1]/text()')
                item_loader.add_xpath('author_name', 'td[@class="tbs"]/div[@class="auth"]/a/text()')
                item_loader.add_xpath('author_url', 'td[@class="tbs"]/div[@class="auth"]/a/@href')
                if good_div.xpath('td[@class="tbs"]/div[3]//span[@class="identify-icon"]'):
                    item_loader.add_xpath('author_identify_depart',
                                          'td[@class="tbs"]/div[3]/div[contains(@class, "expert")]/a/text()')
                    item_loader.add_xpath('author_identify',
                                          'td[@class="tbs"]/div[3]/div[contains(@class, "expert")]/a/@title')
                else:
                    item_loader.add_value('author_identify_depart', '无')
                    item_loader.add_value('author_identify', '无')
                if good_div.xpath('td[@class="tbs"]/div[3]/div[@class="user-level-area"]/text()'):
                    item_loader.add_xpath('author_level',
                                          'td[@class="tbs"]/div[3]/div[@class="user-level-area"]/text()')
                elif good_div.xpath('td[@class="tbs"]/div[3]//span[@class="adm"]/text()'):
                    item_loader.add_xpath('author_level', 'td[@class="tbs"]/div[3]//span[@class="adm"]/text()')
                else:
                    item_loader.add_value('author_level', '其它')
                item_loader.add_xpath('author_scores',
                                      'td[@class="tbs"]/div[@class="user_atten"]/ul/li[1]/div/a/text()')
                item_loader.add_xpath('author_votes', 'td[@class="tbs"]/div[@class="user_atten"]/ul/li[2]/div/a/text()')
                item_loader.add_xpath('author_dingdang',
                                      'td[@class="tbs"]/div[@class="user_atten"]/ul/li[3]/div/a/text()')
                item_loader.add_xpath('vote_num',
                                      'td[@class="tbc"]/div[@class="conbox"]//li[@class="vote-btn"]/span/text()')
                item_loader.add_xpath('fav_num',
                                      'td[@class="tbc"]/div[@class="conbox"]//li[@class="fav-btn"]/span/text()')
                item_loader.add_xpath('reward_num',
                                      'td[@class="tbc"]/div[@class="conbox"]//li[@class="reward-btn"]/span/text()')
                if good_div.xpath('td[@class="tbc"]/div[@class="conbox"]//div[@class="quote"]'):
                    item_loader.add_value('reference_bool', 1)
                else:
                    item_loader.add_value('reference_bool', 0)
                item_loader.add_value('isGood', 1)
                posts_item = item_loader.load_item()
                yield posts_item

        tr_list = response.xpath('//div[starts-with(@id, "post_")]/table/tbody/tr')
        for tr in tr_list:
            item_loader = DingxiangyuanItemLoader(item=PostsRepliesItem(), selector=tr)
            item_loader.add_value('topic_url', topic_url)
            if tr.xpath('td[@class="tbc"]/div[1]/div[1]/ul/div[@class="blt-icon lfloat"]'):
                item_loader.add_value('hot', 1)
            else:
                item_loader.add_value('hot', 0)
            floor = int(
                tr.xpath('td[@class="tbc"]/div[1]/div[1]/ul//span[@class="layer"]/text()').extract_first().strip('楼'))
            item_loader.add_value('floor', floor)
            item_loader.add_value('topic_title', topic_title)
            if floor == 1:
                item_loader.add_value('isTopic', 1)
                item_loader.add_xpath('browser_num',
                                      'td[@class="tbc"]/div[@class="conbox"]//div[@class="post-info"]/span[last()-1]/text()')
                item_loader.add_xpath('reply_num',
                                      'td[@class="tbc"]/div[@class="conbox"]//div[@class="post-info"]/span[last()]/text()')
            else:
                item_loader.add_value('isTopic', 0)
                item_loader.add_value('browser_num', 0)
                item_loader.add_value('reply_num', 0)
            item_loader.add_xpath('content', 'string(td[@class="tbc"]/div[@class="conbox"]//td[@class="postbody"])')
            item_loader.add_value('topic_type', topic_type)  # 主题帖类型
            item_loader.add_value('board_name', board_name)  # 所属板块
            item_loader.add_xpath('post_time',
                                  'td[@class="tbc"]/div[@class="conbox"]//div[@class="post-info"]/span[1]/text()')
            item_loader.add_xpath('author_name', 'td[@class="tbs"]/div[@class="auth"]/a/text()')
            item_loader.add_xpath('author_url', 'td[@class="tbs"]/div[@class="auth"]/a/@href')
            if tr.xpath('td[@class="tbs"]/div[3]//span[@class="identify-icon"]'):
                item_loader.add_xpath('author_identify_depart',
                                      'td[@class="tbs"]/div[3]/div[contains(@class, "expert")]/a/text()')
                item_loader.add_xpath('author_identify',
                                      'td[@class="tbs"]/div[3]/div[contains(@class, "expert")]/a/@title')
            else:
                item_loader.add_value('author_identify_depart', '无')
                item_loader.add_value('author_identify', '无')
            if tr.xpath('td[@class="tbs"]/div[3]/div[@class="user-level-area"]/text()'):
                item_loader.add_xpath('author_level', 'td[@class="tbs"]/div[3]/div[@class="user-level-area"]/text()')
            elif tr.xpath('td[@class="tbs"]/div[3]//span[@class="adm"]/text()'):
                item_loader.add_xpath('author_level', 'td[@class="tbs"]/div[3]//span[@class="adm"]/text()')
            else:
                item_loader.add_value('author_level', '其它')
            item_loader.add_xpath('author_scores', 'td[@class="tbs"]/div[@class="user_atten"]/ul/li[1]/div/a/text()')
            item_loader.add_xpath('author_votes', 'td[@class="tbs"]/div[@class="user_atten"]/ul/li[2]/div/a/text()')
            item_loader.add_xpath('author_dingdang', 'td[@class="tbs"]/div[@class="user_atten"]/ul/li[3]/div/a/text()')
            item_loader.add_xpath('vote_num',
                                  'td[@class="tbc"]/div[@class="conbox"]//li[@class="vote-btn"]/span/text()')
            item_loader.add_xpath('fav_num', 'td[@class="tbc"]/div[@class="conbox"]//li[@class="fav-btn"]/span/text()')
            item_loader.add_xpath('reward_num',
                                  'td[@class="tbc"]/div[@class="conbox"]//li[@class="reward-btn"]/span/text()')
            if tr.xpath('td[@class="tbc"]/div[@class="conbox"]//td[@class="postbody"]/div[@class="quote"]'):
                item_loader.add_value('reference_bool', 1)
            else:
                item_loader.add_value('reference_bool', 0)
            item_loader.add_value('isGood', 0)
            posts_item = item_loader.load_item()
            yield posts_item

    @staticmethod
    def strings_prosses(content):
        return content.strip().replace(' ', '')
