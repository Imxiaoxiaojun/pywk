# -*- coding: utf-8 -*-
import scrapy
from ctbook.items import CtookItem
from ctbook.dbHelper import DBHelper
from pydispatch import dispatcher
from scrapy import signals

class SuluSpider(scrapy.Spider):
    name = 'sulu'
    count = 0
    url_format = "https://www.lbsulu.com/search/12_24_all_all_all_all_onclick_{}.html"
    allowed_domains = ['www.lbsulu.com']
    start_urls = []
    # allowed_domains= ['baidu.com']
    # start_urls= ['https://www.baidu.com']
    base_site = 'https://www.lbsulu.com'

    # headers = {
    #     "HOST": "baidu.com",
    #     "Referer": "www.lbsulu.com",
    # 'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    # }
    def __init__(self):
        self.db = DBHelper()
        self.init_urls()
        dispatcher.connect(self.spider_closed, signals.spider_closed)
    def spider_closed(self, spider):
        print('spider_closed count=',self.count)
        sql = "update `ct_job` set `offset` = {} where `job_type` = 1;".format(self.count)
        self.db.update(sql)
        pass
    def init_urls(self):
        sql = "SELECT offset FROM ct_job WHERE job_type = 1"
        result = self.db.query(sql)
        if not result is None and not result[0] is None:
            self.count = result[0]
        print("before clear urls", self.start_urls)
        # self.start_urls.clear()
        print("after clear urls", self.start_urls)
        for i in range(5):
            url = self.url_format.format(self.count)
            self.count = self.count + 1
            self.start_urls.append(url)
        print("after init urls", self.start_urls)

    def parse(self, response):
        # print("current request url", response.request.url)
        # self.start_urls.clear()
        # print("after urls clear", len(self.start_urls))
        bks = response.css('.indliemh li')
        if bks is None or len(bks) <= 0:
            return
        for bk in bks:
            item = CtookItem()
            item['bkName'] = bk.css('a').css('p::text').extract_first()
            item['bkUrl'] = self.base_site + bk.css('a::attr(href)').extract_first()
            item['bkImg'] = self.base_site + bk.css('img::attr(src)').extract_first()
            description = bk.css('em').css('a::text').extract_first()
            item['bkDesc'] = '' if description is None else description
            print("item:", item)
            yield item
        # next_page_urls = self.base_site + str(
        #     response.css('.pagination-wrapper a').css('.next').css('a::attr(href)').extract_first())
        # print("next page url ", next_page_urls)
        # if next_page_urls.strip() == '':
        #     print("next page is null")
        #     return
        next_page_url = str(self.url_format.format(self.count))
        print("next url", next_page_url)
        self.count = self.count + 1
        print("count = ", self.count)
        yield scrapy.Request(next_page_url, callback=self.parse)
