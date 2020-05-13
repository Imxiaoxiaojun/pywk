import scrapy
from ctbook.dbHelper import DBHelper


class ArticleList(scrapy.Spider):
    name = 'article_list'
    url_format = "https://www.lbsulu.com/search/12_24_all_all_all_all_onclick_{}.html"
    allowed_domains = ['www.lbsulu.com']
    start_urls = []
    base_site = 'https://www.lbsulu.com'

    # headers = {
    #     "HOST": "baidu.com",
    #     "Referer": "www.lbsulu.com",
    # 'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    # }
    def __init__(self):
        self.db = DBHelper()
        pass

    def spider_closed(self, spider):
        print('spider_closed count=', self.count)
        sql = "update `ct_job` set `offset` = {} where `job_type` = 1;".format(self.count)
        self.db.update(sql)
        pass

    def init_urls(self):
        pass

    def parse(self, response):
        pass