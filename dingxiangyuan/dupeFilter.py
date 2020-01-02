# -*- coding:utf-8 _*-
"""
@author: Zhang Yafei
@time: 2019/11/{DAY}
"""
from scrapy_redis.dupefilter import RFPDupeFilter
from scrapy.http.request import Request


class RedisDupeFilter(RFPDupeFilter):

    @classmethod
    def from_crawler(cls, crawler):
        """Returns instance from crawler.

        Parameters
        ----------
        crawler : scrapy.crawler.Crawler

        Returns
        -------
        RFPDupeFilter
            Instance of RFPDupeFilter.

        """
        return cls.from_settings(crawler.settings)

    def request_seen(self, request: Request) -> bool:
        """Returns True if request was already seen else False"""
        fp = self.request_fingerprint(request)
        added = self.server.sismember(self.key, fp)
        return added
