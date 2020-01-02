# -*- coding:utf-8 -*-
"""
@author:Zhang Yafei
@time: 2019/12/06
"""
import os
import sys
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(__file__))


def run(job):
    execute(['scrapy', 'crawl', job])
    # execute(['scrapy', 'crawl', job, "--nolog"])


if __name__ == '__main__':
    # run(job="board")
    # run(job="topics")
    # run(job="posts_replies")
    run(job="dingxiangke")
    # run(job="topic_rate")