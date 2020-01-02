# -*- coding:utf-8 _*-
"""
@author:Zhang Yafei
@time: 2019/12/02
"""
from urllib.parse import unquote

import pandas as pd
from redis import ConnectionPool, Redis
from scrapy.utils.project import get_project_settings
from dingxiangyuan import settings
from sqlalchemy import create_engine
from DBUtils.PooledDB import PooledDB


class DBPoolHelper(object):
    def __init__(self, dbname, user=None, password=None, db_type='postgressql', host='localhost', port=5432):
        """
        # sqlite3
        # 连接数据库文件名，sqlite不支持加密，不使用用户名和密码
        import sqlite3
        config = {"datanase": "path/to/your/dbname.db"}
        pool = PooledDB(sqlite3, maxcached=50, maxconnections=1000, maxusage=1000, **config)
        # mysql
        import pymysql
        pool = PooledDB(pymysql,5,host='localhost', user='root',passwd='pwd',db='myDB',port=3306) #5为连接池里的最少连接数
        # postgressql
        import psycopg2
        POOL = PooledDB(creator=psycopg2, host="127.0.0.1", port="5342", user, password, database)
        # sqlserver
        import pymssql
        pool = PooledDB(creator=pymssql, host=host, port=port, user=user, password=password, database=database, charset="utf8")
        :param type:
        """
        if db_type == 'postgressql':
            import psycopg2
            pool = PooledDB(creator=psycopg2, host=host, port=port, user=user, password=password, database=dbname)
        elif db_type == 'mysql':
            import pymysql
            pool = PooledDB(pymysql, 5, host='localhost', user='root', passwd='pwd', db='myDB',port=3306)  # 5为连接池里的最少连接数
        elif db_type == 'sqlite':
            import sqlite3
            config = {"datanase": dbname}
            pool = PooledDB(sqlite3, maxcached=50, maxconnections=1000, maxusage=1000, **config)
        else:
            raise Exception('请输入正确的数据库类型, db_type="postgresql" or db_type="mysql" or db_type="sqlite"' )
        self.conn = pool.connection()
        self.cursor = self.conn.cursor()

    def connect_close(self):
        """关闭连接"""
        self.cursor.close()
        self.conn.close()

    def execute(self, sql, params=tuple()):
        self.cursor.execute(sql, params)  # 执行这个语句
        self.conn.commit()

    def fetchone(self, sql, params=tuple()):
        self.cursor.execute(sql, params)
        data = self.cursor.fetchone()
        return data

    def fetchall(self, sql, params=tuple()):
        self.cursor.execute(sql, params)
        data = self.cursor.fetchall()
        return data


def pandas_db_helper():
    """
    'postgresql://postgres:0000@127.0.0.1:5432/xiaomuchong'
    "mysql+pymysql://root:0000@127.0.0.1:3306/srld?charset=utf8mb4"
    "sqlite: ///sqlite3.db"
    """
    engine = create_engine(settings.DATABASE_ENGINE)
    conn = engine.connect()
    return conn


def redis_init():
    settings = get_project_settings()
    if settings["REDIS_PARAMS"]:
        pool = ConnectionPool(host=settings["REDIS_HOST"], port=settings["REDIS_PORT"],
                              password=settings["REDIS_PARAMS"]['password'])
    else:
        pool = ConnectionPool(host=settings["REDIS_HOST"], port=settings["REDIS_PORT"])
    conn = Redis(connection_pool=pool)
    return conn


redis_conn = redis_init()
db_conn = pandas_db_helper()


def cal_page_url(row):
    topic_url, reply_num = row[0], row[1]
    page_num = reply_num // 35 + 1
    redis_conn.sadd('topic_page_urls', topic_url)
    for page in range(2, page_num + 1):
        redis_conn.sadd('topic_page_urls', f'{topic_url}?ppg={page}')
    print(topic_url)


def insert_redis_topic_page_urls():
    data = pd.read_sql(sql="topics", con=db_conn, columns=["topic_url", "reply_num"])
    data.apply(cal_page_url, axis=1)


def get_topic_left_start_urls():
    topic_urls = pd.read_sql(sql="select distinct topic_url from posts_replies", con=db_conn)
    topic_urls_floor_one = pd.read_sql(sql="select topic_url from posts_replies where floor=1", con=db_conn)
    has_topic_urls = set(topic_urls['topic_url']) - set(topic_urls_floor_one['topic_url'])
    topic_page_urls = redis_conn.smembers('topic_page_urls')
    start_urls = {url.decode() for url in topic_page_urls if url.decode().split('?')[0] in has_topic_urls}
    print(len(has_topic_urls), len(start_urls))


def get_user_start_urls():
    """ 获取用户表起始url """
    user_urls = pd.read_sql(sql="select distinct author_url from posts_replies", con=db_conn)
    moderator_urls = pd.read_sql(sql="select distinct moderator_url_list from board", con=db_conn)
    moderator_urls_list = [url for moderator_list in moderator_urls['moderator_url_list'].str.split('; ') for url in moderator_list]
    for url in user_urls['author_url']:
        redis_conn.sadd('dingxiangke_start_urls', url)
    for url in moderator_urls_list:
        redis_conn.sadd('dingxiangke_start_urls', url)
    print('添加完成')


def insert_into_topic_rate():
    """ 插入积分表 """
    postgres = DBPoolHelper(db_type='postgressql', dbname='dingxiangyuan', user='postgres', password='0000', host='localhost', port='5432')
    data1 = pd.read_sql(sql="select topic_url from posts_replies where floor=1", con=db_conn)
    data2 = pd.read_sql(sql="select topic_url from topic_rate_get", con=db_conn)
    topic_urls = set(data1['topic_url']) - set(data2['topic_url'])
    for topic_url in topic_urls:
        res = pd.read_sql(sql='select topic_type, board_name from posts_replies where floor=1 and topic_url=%s', con=db_conn, params=(topic_url,))
        topic_type, board_name = res['topic_type'].values[0], res['board_name'].values[0]
        try:
            postgres.execute(sql="INSERT INTO topic_rate_get(topic_url, topic_type, board_name, rate_get) VALUES(%s, %s, %s, 0)", params=(topic_url, topic_type, board_name))
            print('插入成功')
        except Exception as e:
            print('插入失败', e)
    postgres.connect_close()


def delete_empty_topic_url():
    """ 删除主题帖不存在的回复 """
    postgres = DBPoolHelper(db_type='postgressql', dbname='dingxiangyuan', user='postgres', password='0000', host='localhost', port='5432')
    data1 = pd.read_sql('select topic_url from posts_replies where floor=1', con=db_conn)
    data2 = pd.read_sql('select distinct topic_url from posts_replies', con=db_conn)
    topic_urls = set(data2['topic_url']) - set(data1['topic_url'])
    # topic_urls = {'http://www.dxy.cn/bbs/topic/16938569', 'http://www.dxy.cn/bbs/topic/30229085', 'http://www.dxy.cn/bbs/topic/16568390', 'http://www.dxy.cn/bbs/topic/36096787', 'http://www.dxy.cn/bbs/topic/15125086', 'http://www.dxy.cn/bbs/topic/17948811', 'http://www.dxy.cn/bbs/topic/25201985', 'http://cardiovascular.dxy.cn/bbs/topic/36725028', 'http://www.dxy.cn/bbs/topic/7716905', 'http://www.dxy.cn/bbs/topic/14908986', 'http://www.dxy.cn/bbs/topic/40363469', 'http://www.dxy.cn/bbs/topic/25248231', 'http://www.dxy.cn/bbs/topic/11875242', 'http://cardiovascular.dxy.cn/bbs/topic/29575155', 'http://chest.dxy.cn/bbs/topic/11838188', 'http://www.dxy.cn/bbs/topic/18213734', 'http://www.dxy.cn/bbs/topic/1546642', 'http://www.dxy.cn/bbs/topic/28689847', 'http://www.dxy.cn/bbs/topic/24223943', 'http://www.dxy.cn/bbs/topic/11647123'}
    # print(len(topic_urls))
    for url in topic_urls:
        try:
            postgres.execute('delete from posts_replies where topic_url=%s', params=(url,))
            print('删除成功')
        except Exception as e:
            print('删除失败', e)
    postgres.connect_close()


def update_user_url():
    """ 更新用户url """
    postgres = DBPoolHelper(db_type='postgressql', dbname='dingxiangyuan', user='postgres', password='0000', host='localhost', port='5432')

    def url_unquote(url):
        global Num
        unquote_url = unquote(url)
        print(url, unquote_url)
        try:
            postgres.execute(sql='update dingxiangke set user_url_unquote=%s where user_url=%s',
                             params=(unquote_url, url))
            Num += 1
            print('更新成功', Num)
        except Exception as e:
            print('更新失败', e)

    data = pd.read_sql(sql='select distinct user_url from dingxiangke', con=db_conn)
    data['user_url'].apply(url_unquote)


def delete_user_invalid_posts():
    postgres = DBPoolHelper(db_type='postgressql', dbname='dingxiangyuan', user='postgres', password='0000', host='localhost', port='5432')
    data1 = pd.read_sql(sql='select distinct author_url from posts_replies', con=db_conn)
    data2 = pd.read_sql(sql='select distinct user_url_unquote from dingxiangke', con=db_conn)
    author_urls = set(data1['author_url']) - set(data2['user_url_unquote'])
    # user_urls = set(data2['user_url_unquote']) - set(data1['author_url'])
    # print(len(author_urls), len(user_urls))
    for user_url in author_urls:
        try:
            postgres.execute(sql='delete from posts_replies where author_url=%s', params=(user_url,))
            print('删除成功', user_url)
        except Exception as e:
            print('删除失败', e)
    postgres.connect_close()


def calc_board_size():
    """ 计算社区规模 """
    data1 = pd.read_sql(sql='''select board_name board, to_char(post_time, 'YYYY') as year, count(distinct topic_url) as topics_nums from posts_replies where floor=1 GROUP BY board_name, year''', con=db_conn)
    data2 = pd.read_sql(sql='''select board_name board, to_char(post_time, 'YYYY') as year, count(distinct author_url) users_num from posts_replies GROUP BY board_name, year;''', con=db_conn)
    data = pd.merge(data2, data1, on=['board', 'year'])

    def board_size(row):
        return round(row.users_num / row.topics_nums, 4)

    data['board_size'] = data.apply(board_size)
    data.to_excel('res/env_board_size.xlsx', engine='xlsxwriter', index=False)


def calc_board_members_level_quality():
    """ 计算社区板块成员质量 """
    data_list = []
    board_names = ['心血管', '呼吸胸外', '肿瘤医学', '神经内外', '危重急救', '内分泌', '消化内科', '肾脏泌尿', '感染']
    for board in board_names:
        data = pd.read_sql(sql='''select board_name, to_char(posts_replies.post_time, 'YYYY') as year, user_level, count(distinct dingxiangke.user_url) user_count,sum(dingxiangke.posts) 用户总发帖数 from dingxiangke
                                    inner join posts_replies on posts_replies.author_url=dingxiangke.user_url_unquote
                                    where posts_replies.board_name=%s
                                    GROUP BY board_name, year, user_level''', con=db_conn, params=(board, ))

        for year in data.year.unique():
            user_nums = data.loc[data.year == year, 'user_count'].sum()
            high_user_nums = data.loc[(data.year == year) & (~data.user_level.isin(['常驻站友', '入门站友', '铁杆站友'])), 'user_count'].sum()
            high_user_prop = round(high_user_nums / user_nums, 4)
            data_list.append({'board': board, 'year': year, 'high_user_prop': high_user_prop})

    df = pd.DataFrame(data=data_list)
    df.to_excel('res/borad_user_quality.xlsx', index=False, engine='xlsxwriter')
    # df.to_csv('res/borad_user_quality.csv', index=False, encoding='utf_8_sig')


def calc_board_members_identify_quality():
    """ 计算社区板块成员质量 """
    data_list = []
    board_names = ['心血管', '呼吸胸外', '肿瘤医学', '神经内外', '危重急救', '内分泌', '消化内科', '肾脏泌尿', '感染']
    for board in board_names:
        data = pd.read_sql(sql='''select board_name, to_char(posts_replies.post_time, 'YYYY') as year, author_identify, count(distinct dingxiangke.user_url) user_count from dingxiangke
                            inner join posts_replies on posts_replies.author_url=dingxiangke.user_url_unquote
                            where posts_replies.board_name='心血管'
                            GROUP BY board_name, year, author_identify''', con=db_conn, params=(board, ))

        for year in data.year.unique():
            user_nums = data.loc[data.year == year, 'user_count'].sum()
            certified_prop = data.loc[(data.year == year) & (data.author_identify != '无'), 'user_count'].sum()
            high_user_prop = round(certified_prop / user_nums, 4)
            data_list.append({'board': board, 'year': year, 'certified_user_prop': high_user_prop})

    df = pd.DataFrame(data=data_list)
    df.to_excel('res/borad_certified_user.xlsx', index=False, engine='xlsxwriter')


def select_env_factor_sys_op():
    """ 查询环境因素系统操控（精华帖占比和积分占比） """
    data = pd.read_sql(sql='''SELECT posts_replies.board_name, to_char(posts_replies.post_time, 'YYYY') as year, sum(topics.good_topic) good_topic_nums, sum(topic_rate_get.rate_get) rate_sum, count(*), round(sum(topics.good_topic)::numeric/count(*)::numeric,4) good_topic_prop, round(sum(topic_rate_get.rate_get)::numeric/count(*)::numeric,4) post_rate_prop from posts_replies 
                        left join topics on posts_replies.topic_url=topics.topic_url 
                        left join topic_rate_get on topic_rate_get.topic_url=posts_replies.topic_url
                        where posts_replies.floor=1 group by posts_replies.board_name, year;''', con=db_conn)
    data.to_excel('res/env_factor_sys_op.xlsx', index=False, engine='xlsxwriter')


def data_merge():
    certified_user_df = pd.read_excel('res/board_certified_user.xlsx')
    user_level_df = pd.read_excel('res/board_user_quality.xlsx')
    env_board_size_df = pd.read_excel('res/env_board_size.xlsx')
    env_factor_sys_op_df = pd.read_excel('res/env_factor_sys_op.xlsx')
    env_factor_df = pd.read_excel('res/环境因素查询.xlsx')
    input_output_df = pd.read_excel('res/投入产出指标查询.xlsx')
    input_output_df2 = pd.read_excel('res/投入产出指标查询2.xlsx')


if __name__ == '__main__':
    # 计算page_urls，并将page_urls插入redis
    # insert_redis_topic_page_urls()
    # 获取起始url
    # get_topic_left_start_urls()
    # get_user_start_urls()
    # 插入帖子积分表
    # insert_into_topic_rate()
    # 删除无效帖子
    # delete_empty_topic_url()
    # 更新作者url地址
    # Num = 0
    # update_user_url()
    # 删除无效用户帖子
    # delete_user_invalid_posts()
    # 计算板块社区成员质量
    # calc_board_members_level_quality()
    # calc_board_members_identify_quality()
    # 查询环境因素系统操控占比
    # select_env_factor_sys_op()
    # 计算社区规模
    # calc_board_size()
    # 合并数据
    data_merge()