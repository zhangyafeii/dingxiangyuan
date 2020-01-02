# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from twisted.enterprise import adbapi
import pymongo
from twisted.internet import reactor, defer
import psycopg2


class MongoPipline(object):
    """
    异步插入MongoDB
    """
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI', 'mongodb://127.0.0.1:27017/'),
            mongo_db=crawler.settings.get('MONGO_DB'),
        )

    def open_spider(self, spider):
        """
        爬虫启动时，启动
        :param spider:
        :return:
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.mongodb = self.client[self.mongo_db]

    def close_spider(self, spider):
        """
        爬虫关闭时执行
        :param spider:
        :return:
        """
        self.client.close()

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        out = defer.Deferred()
        reactor.callInThread(self._insert, item, out, spider)
        yield out
        defer.returnValue(item)

    def _insert(self, item, out, spider):
        """
        插入函数
        :param item:
        :param out:
        :return:
        """
        self.mongodb[spider.name].insert(dict(item))
        reactor.callFromThread(out.callback, item)


class PostgresSQLPipeline(object):
    """ PostgreSQL pipeline class """
    def __init__(self, dbpool):
        self.logger = logging.getLogger()
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['POSTGRESQL_HOST'],
            database=settings['POSTGRESQL_DATABASE'],
            user=settings['POSTGRESQL_USER'],
            password=settings['POSTGRESQL_PASSWORD'],
        )
        dbpool = adbapi.ConnectionPool('psycopg2', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._insert_item, item)
        d.addErrback(self._handle_error, item, spider)

    def _insert_item(self, cursor, item):
        """Perform an insert or update."""
        insert_sql, params = item.get_insert_sql()
        try:
            cursor.execute(insert_sql, params)
            print('插入成功')
        except psycopg2.errors.UniqueViolation:
            print('数据重复插入，跳过')
        except Exception as e:
            self.logger.error('插入失败', e)

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        self.logger.error(failure)