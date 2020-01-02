# -*- coding: utf-8 -*-
import scrapy
from dingxiangyuan.items import DingxiangyuanItemLoader, TopicsItem
from dingxiangyuan import settings


class TopicsSpider(scrapy.Spider):
    name = 'topics'
    allowed_domains = ['www.dxy.cn', 'neuro.dxy.cn', 'chest.dxy.cn', 'cardiovascular.dxy.cn']
    # start_urls = ['http://www.dxy.cn/bbs/board/87?tpg=145']
    # start_urls = [f'http://cardiovascular.dxy.cn/bbs/board/47?tpg={num}' for num in range(1, 1000)]   # 心血管
    # start_urls = [f'http://www.dxy.cn/bbs/board/87?tpg={num}' for num in range(1, 1001)]              # 恶性肿瘤
    # start_urls = [f'http://chest.dxy.cn/bbs/board/58?tpg={num}' for num in range(1, 1001)]            # 呼吸胸外
    # start_urls = [f'http://www.dxy.cn/bbs/board/112?tpg={num}' for num in range(1, 1001)]             # 急救与危重病
    # start_urls = [f'http://www.dxy.cn/bbs/board/92?tpg={num}' for num in range(1, 1001)]              # 内分泌
    # start_urls = [f'http://www.dxy.cn/bbs/board/188?tpg={num}' for num in range(1, 1001)]             # 消化内科
    # start_urls = [f'http://neuro.dxy.cn/bbs/board/46?tpg={num}' for num in range(1, 1001)]            # 神经系统
    # start_urls = [f'http://www.dxy.cn/bbs/board/49?tpg={num}' for num in range(1, 1001)]              # 泌尿生殖
    start_urls = [f'http://www.dxy.cn/bbs/board/146?tpg={num}' for num in range(1, 811)]             # 感染

    # @staticmethod
    # def get_start_urls():
    #     """ 获取起始url """
    #     for board_url in settings.BOARD_MAP:
    #         yield [f'{board_url}-{page}' for page in range(1, 201)]
    #
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        tr_list = response.xpath('//tr[contains(@class, "hoverClass")]')
        board_id = settings.BOARD_MAP[response.url.rsplit('?', maxsplit=1)[0]][0]
        board_name = settings.BOARD_MAP[response.url.rsplit('?', maxsplit=1)[0]][1]
        for tr in tr_list:
            item_loader = DingxiangyuanItemLoader(item=TopicsItem(), selector=tr)
            item_loader.add_xpath('topic_url', 'td[@class="news"]/a[starts-with(@href, "http://")]/@href')
            if response.xpath('string(td[@class="news"]/a[starts-with(@href, "http://")])'):
                item_loader.add_xpath('topic_title', 'string(td[@class="news"]/a[starts-with(@href, "http://")])')
            else:
                item_loader.add_value('topic_title', '空')
            item_loader.add_value('board_id', board_id)
            item_loader.add_value('board_name', board_name)
            item_loader.add_xpath('author_name', 'td[@class="by"]/a/text()')
            if tr.xpath('td[@class="news"]/span[contains(@class, "icon-case")]'):
                item_loader.add_value('case_topic', 1)
            else:
                item_loader.add_value('case_topic', 0)
            if tr.xpath('td[@class="news"]/span[contains(@class, "icon-good")]'):
                item_loader.add_value('good_topic', 1)
            else:
                item_loader.add_value('good_topic', 0)
            if tr.xpath('td[@class="news"]/span[contains(@class, "icon-recommend")]'):
                item_loader.add_value('recommend_topic', 1)
            else:
                item_loader.add_value('recommend_topic', 0)
            if tr.xpath('td[@class="news"]/span[contains(@class, "icon-award")]'):
                item_loader.add_value('award_topic', 1)
            else:
                item_loader.add_value('award_topic', 0)
            item_loader.add_xpath('author_url', 'td[@class="by"]/a/@href')
            item_loader.add_xpath('post_time', 'td[@class="by"]/em/text()')
            item_loader.add_xpath('reply_num', 'td[@class="num calign"]/a/text()')
            item_loader.add_xpath('click_num', 'td[@class="num calign"]/em/text()')
            item_loader.add_xpath('last_reply_time', 'td[@class="by ralign last"]/em/text()')
            topic_item = item_loader.load_item()
            yield topic_item


