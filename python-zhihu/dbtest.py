# -*- coding: utf-8 -*-
from collections import Counter
from DBUtil import Mysql


if __name__ == '__main__':
    mysql = Mysql()
    userList = []
    # userList.append({'avatar_url':'123123','avatar_url_template':'asdfsdf','gender':1,'headline':'asdflksajdf','id':'1231sadflkj','is_advertiser':'false','name':'saf'+str(i),'type':'person','url':'adfalkdjf','url_token':'asfsaf','user_type':'asdfj'})
    userList.append(['nihao'])
    userList.append(['nihaoasfasdf'])

    sql = 'insert into python.zh_user(name) VALUES (%s)'
    mysql.insertMany(sql, userList)
    mysql.end('commit')