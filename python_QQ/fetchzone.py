# -*- coding:utf-8 -*-
import csv
import re
import cookielib
import urllib2
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Fetch(object):
    def __init__(self):
        # 指定图片目录
        try:
            self.qq_list = []
            csv_reader = csv.reader(open('./source/QQmail.csv'))
            for line in csv_reader:
                mail = str(line).split(',')[3]
                if mail.find('@') != -1:
                    try:
                        e_mail = int(mail.strip()[1:mail.rfind('@')-1])
                        self.qq_list.append(e_mail)
                    except:
                        continue
        except Exception, e:
            print e

    def get_talk(self, qq):
        # url = 'https://user.qzone.qq.com/' + qq + '311'
        url = 'https://user.qzone.qq.com/337433736/infocenter'
        rep = urllib2.urlopen(urllib2.Request(url))
        if rep.code != 200:
            print rep.code
        else:
            print rep.read().decode('UTF-8', 'ignore')


if __name__ == '__main__':
    # fetch = Fetch()
    # print fetch.get_talk('351447282')
    # for i in range(len(fetch.qq_list)):
    #     print fetch.qq_list[i]
    url = 'http://user.qzone.qq.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36', }
    # 这块可以通过抓包工具来获得
    postData = {
        'log': '727877397',
        'pwd': 'yzz!123',
        'wp-submit': '登录',
        'redirect_to': 'https://user.qzone.qq.com/337433736/infocenter',
        'testcookie': '1'
    }

    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    h = urllib2.urlopen(url)

    postData = urllib.urlencode(postData)
    request = urllib2.Request(url, postData, headers)
    response = urllib2.urlopen(request)
    text = response.read().decode('utf-9')
    print text
