# -*- coding:utf-8 -*-
"""
@author: Zhang Yafei
@time: 2019/11/30
"""
from redis import Redis, ConnectionPool

# 连接池
pool = ConnectionPool(host='127.0.0.1', port=6379)
conn = Redis(connection_pool=pool)
print(conn.keys())
# print(conn.exists("post_urls"))

# 查看队列
# print(conn.lrange("charmer:items", 0, -1))
# 查看集合
# print(conn.smembers("topics:dupefilter"))
# print(conn.smembers("board:dupefilter"))

# 查看集合长度
# print(conn.scard("board:dupefilter"))
# print(conn.scard("topics:dupefilter"))
# print(conn.scard("posts_replies:dupefilter"))
# print(conn.scard("topic_page_urls"))
print(conn.scard("dingxiangke_start_urls"))
print(conn.scard('dingxiangke:dupefilter'))
print(conn.scard('dingxiangke_error_url'))
print(conn.scard('topic_rate:dupefilter'))
# print(conn.smembers("posts_replies_error_url"))
# print(conn.scard("posts_replies_error_url"))

# 查看集合元素
# print(conn.smembers('team:dupefilter'))
# 查看是否是集合成员
# print(conn.sismember('team:dupefilter', '9ff5702d6a40f5949a1dbd79955f999268c38761'))
# 集合运算
# print(conn.sdiff("posts_visit_urls", "posts_page_urls"))
# print(conn.sdiff("posts_page_urls", "posts_visit_urls"))
# 删除键
# conn.delete('posts:dupefilter')
# conn.delete('comments:dupefilter')
# conn.delete('comments:error')
# conn.delete('comment_url')
# conn.delete('board:dupefilter')
# conn.delete('topics:dupefilter')
# conn.delete('posts_replies:dupefilter')
# conn.delete('posts_replies_error_url')
# conn.delete('dingxiangke:dupefilter')
# conn.delete('dingxiangke_error_url')
# conn.delete('topic_rate:dupefilter')


# conn.delete('posts:error')
# conn.delete('posts_urls')
# conn.delete('posts_visit_urls')
# conn.delete('posts:error')
# conn.delete('team:dupefilter')
# conn.delete("<PostsSpider 'posts' at 0x4b0fe88>:error")
# conn.flushall()
# print(conn.keys())
