# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join


class TakeFirstCustom(TakeFirst):
    def __call__(self, values):
        for value in values:
            return value


class DingxiangyuanItemLoader(ItemLoader):
    # default_output_processor = TakeFirst()
    default_output_processor = TakeFirstCustom()


def get_topic_num(value):
    return int(value.strip('主题：'))


class BoardItem(scrapy.Item):
    """ 板块信息表 """
    board_id = scrapy.Field()
    board_name = scrapy.Field()
    board_url = scrapy.Field()
    topic_num = scrapy.Field(input_processor=MapCompose(get_topic_num))
    moderator_url_list = scrapy.Field(input_processor=Join('; '))

    def get_insert_sql(self):
        insert_sql = """
            insert into board(board_id, board_name, board_url, topic_num, moderator_url_list)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (self['board_id'], self["board_name"], self["board_url"], self['topic_num'], self["moderator_url_list"])
        return insert_sql, params


def date_convert(value):
    date = datetime.datetime.strptime(value, "%Y-%m-%d").date()
    return date


def datetime_convert(value):
    date_time = datetime.datetime.strptime(value, "%m-%d %H:%M")
    return date_time


def datetime_convert2(value):
    date_time = datetime.datetime.strptime(value[0], "%Y-%m-%d %H:%M")
    return date_time


class TopicsItem(scrapy.Item):
    """ 帖子表 """
    topic_url = scrapy.Field()
    topic_title = scrapy.Field()
    board_id = scrapy.Field(input_processor=MapCompose(int))
    board_name = scrapy.Field()
    case_topic = scrapy.Field()       # 病历帖
    good_topic = scrapy.Field()       # 精华帖
    recommend_topic = scrapy.Field()  # 推荐帖
    award_topic = scrapy.Field()      # 悬赏帖
    author_name = scrapy.Field()
    author_url = scrapy.Field()
    post_time = scrapy.Field(input_processor=MapCompose(date_convert))
    reply_num = scrapy.Field(input_processor=MapCompose(int))
    click_num = scrapy.Field(input_processor=MapCompose(int))
    last_reply_time = scrapy.Field(input_processor=MapCompose(datetime_convert))

    def get_insert_sql(self):
        insert_sql = """
             insert into topics(topic_url, topic_title, board_id, board_name, author_name, case_topic, good_topic, recommend_topic, award_topic, author_url, post_time, reply_num, click_num, last_reply_time)
             VALUES (%s, %s, %s, %s, %s,%s, %s,%s,%s, %s, %s, %s, %s, %s)
         """
        params = (self['topic_url'], self['topic_title'], self['board_id'], self["board_name"], self["author_name"],
                  self['case_topic'], self['good_topic'], self['recommend_topic'], self['award_topic'],
                  self['author_url'], self["post_time"], self['reply_num'], self['click_num'], self['last_reply_time'])
        return insert_sql, params


def content_process(value):
    value = value[0].strip().replace('\n', '')
    return value


def get_borwser_reply_num(value):
    value = value.split(':')[1].strip() if value != 0 else value
    return int(value)


def get_num(value):
    value = value if len(value.strip()) >= 1 else 0
    return int(value)


def digit_convert(value):
    if "万" in value:
        return int(float(value.strip('万'))*10000)
    return int(value)


class PostsRepliesItem(scrapy.Item):
    floor = scrapy.Field()
    topic_url = scrapy.Field()
    topic_title = scrapy.Field()
    content = scrapy.Field(output_processor=content_process)
    topic_type = scrapy.Field()
    board_name = scrapy.Field()
    author_name = scrapy.Field()
    author_url = scrapy.Field()
    post_time = scrapy.Field(output_processor=datetime_convert2)
    reference_bool = scrapy.Field()
    author_identify_depart = scrapy.Field()
    author_identify = scrapy.Field()
    author_level = scrapy.Field()
    author_scores = scrapy.Field(input_processor=MapCompose(digit_convert))
    author_votes = scrapy.Field(input_processor=MapCompose(digit_convert))
    author_dingdang = scrapy.Field(input_processor=MapCompose(digit_convert))
    browser_num = scrapy.Field(input_processor=MapCompose(get_borwser_reply_num))
    reply_num = scrapy.Field(input_processor=MapCompose(get_borwser_reply_num))
    vote_num = scrapy.Field(input_processor=MapCompose(get_num))
    fav_num = scrapy.Field(input_processor=MapCompose(get_num))
    reward_num = scrapy.Field(input_processor=MapCompose(get_num))
    isTopic = scrapy.Field()
    isGood = scrapy.Field()
    hot = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
             insert into posts_replies(floor, topic_url, topic_title,content, topic_type,board_name,author_name, author_url,post_time,
                 reference_bool, author_identify_depart, author_identify, author_level,author_scores,author_votes,author_dingdang,browser_num,
                 reply_num, vote_num,fav_num,reward_num,istopic,isgood,hot)
             VALUES (%s, %s, %s, %s, %s,%s, %s,%s,%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
         """
        params = (self['floor'], self['topic_url'], self['topic_title'], self["content"], self["topic_type"],
                  self['board_name'], self['author_name'], self['author_url'], self['post_time'], self['reference_bool'],
                  self['author_identify_depart'], self["author_identify"], self['author_level'], self['author_scores'], self['author_votes'],
                  self['author_dingdang'], self['browser_num'],self['reply_num'],self['vote_num'], self['fav_num'], self['reward_num'],
                  self['isTopic'], self['isGood'], self['hot'])
        return insert_sql, params


def get_user_num(value):
    return int(value.replace('次', '').strip('小时'))


class DingXiangKeItem(scrapy.Item):
    user_url = scrapy.Field()
    user_url_unquote = scrapy.Field()
    user_name = scrapy.Field()
    posts = scrapy.Field(input_processor=MapCompose(int))
    distilled = scrapy.Field(input_processor=MapCompose(int))
    score = scrapy.Field(input_processor=MapCompose(int))
    posts_voted = scrapy.Field(input_processor=MapCompose(int))
    following = scrapy.Field(input_processor=MapCompose(int))
    follower = scrapy.Field(input_processor=MapCompose(int))
    dingdang = scrapy.Field(input_processor=MapCompose(int))
    user_level = scrapy.Field()
    user_identify = scrapy.Field(output_processor=content_process)
    user_city = scrapy.Field()
    posts_browsered = scrapy.Field(input_processor=MapCompose(get_user_num))
    posts_faved = scrapy.Field(input_processor=MapCompose(get_user_num))
    online_time = scrapy.Field(input_processor=MapCompose(get_user_num))

    def get_insert_sql(self):
        insert_sql = """
                INSERT INTO dingxiangke(user_url, user_url_unquote, user_name, posts, distilled, score, posts_voted, following, follower, dingdang,
                    user_level, user_identify, user_city, posts_browsered, posts_faved, online_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        params = (self['user_url'], self['user_url_unquote'], self['user_name'], self['posts'], self["distilled"], self["score"],
                  self['posts_voted'], self['following'], self['follower'], self['dingdang'], self['user_level'],
                  self['user_identify'], self["user_city"], self['posts_browsered'], self['posts_faved'], self['online_time'])
        return insert_sql, params


class TopicRateItem(scrapy.Item):
    topic_url = scrapy.Field()
    topic_type = scrapy.Field()
    board_name = scrapy.Field()
    rate_get = scrapy.Field()

    def get_insert_sql(self):
        """
        INSERT INTO topic_rate_get(topic_url, topic_type, board_name, rate_get) VALUES(%s,%s,%s,%s) ON CONFLICT (topic_url)
        DO UPDATE SET rate_get = EXCLUDED.rate_get;
        """
        update_sql = """
            INSERT INTO topic_rate_get(topic_url, topic_type, board_name, rate_get) VALUES(%s,%s,%s,%s);
        """
        params = (self['topic_url'], self['topic_type'], self['board_name'], self['rate_get'])
        return update_sql, params