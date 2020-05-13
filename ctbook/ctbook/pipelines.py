# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from ctbook.dbHelper import DBHelper

class CtbookPipeline:
    # connection = None
    # cursor = None

    def __init__(self):
    #     # connection database
    #     # get cursor
    #     # 建立数据库连接
    #     self.connection = pymysql.connect(host='127.0.0.1', port=3306, user='manage', password='spdb1234', db='slife',
    #                                       charset='utf8')
    #     #     #创建操作游标
    #     self.cursor = self.connection.cursor()
        self.db = DBHelper()
    #     print("连接数据库成功")

    # def process_item(self, item, spider):
    #     #建立数据库连接
    #     self.connection = pymysql.connect(host='127.0.0.1', port=3306, user='manage', password='spdb1234', db='slife',charset='utf8')
    #     #创建操作游标
    #     self.cursor = self.connection.cursor()
    #     return item

    def process_item(self, item, spider):
        # 定义sql语句
        sql = "INSERT INTO `ct_book` (`bk_hot_news`, `bk_img`, `bk_name`, `bk_url`) VALUES (%s,%s,%s,%s);"
        print("sql = ", sql)
        params=(item['bkDesc'], item['bkImg'], item['bkName'], item['bkUrl'])
        # 执行sql语句
        self.db.insert(sql, *params)
        # self.cursor.execute(sql)
        # 保存修改
        # self.connection.commit()

        return item

    # def __del__(self):
    #     # 关闭操作游标
    #     self.cursor.close()
    #     # 关闭数据库连接
    #     self.connection.close()
