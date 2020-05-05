# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CtookItem(scrapy.Item):
    # define the fields for your item here like:
    # 书名
    bkName = scrapy.Field()
    # 书的链接
    bkUrl = scrapy.Field()
    bkImg = scrapy.Field()
    bkDesc = scrapy.Field()
    bkType = scrapy.Field()
    # 章节名称
    # chtName = scrapy.Field()
    # 章节链接
    # chtUrl = scrapy.Field()
    # pageUrl = scrapy.Field()
    # pass
