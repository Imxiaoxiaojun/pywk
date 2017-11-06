# -*- coding: utf-8 -*-
import requests
import time
from bs4 import BeautifulSoup
import os
from pybloom import BloomFilter
import json
from DBUtil import Mysql

# url = 'https://www.zhihu.com/login/phone_num'


class ZhiHu(object):
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                        'Accept - Encoding': 'gzip, deflate, br',
                        'accept': 'application/json, text/plain, */*'
                        }
        self.cookie = {}
        self.cookies = {}
        self.rList = []

    def get_captcha(self):
        captcha_content = self.session.get('https://www.zhihu.com/captcha.gif?r=%d&type=login' % (time.time() * 1000),
                                           headers=self.headers).content
        with open('captcha.gif', 'wb') as fb:
            fb.write(captcha_content)
        captcha = raw_input('please input captcha in next line↓\n>')
        return captcha

    def login(self, username, password):
        # xyz = self.session.get('https://www.zhihu.com/#signin', headers=self.headers).content
        _xsrf = BeautifulSoup(self.session.get('https://www.zhihu.com/#signin', headers=self.headers).content,
                              'html.parser').find(
            'input', attrs={'name': '_xsrf'}).get('value')
        data = {
            "_xsrf": _xsrf,
            "phone_num": username,
            "password": password,
            "remember_me": True,
            "captcha": self.get_captcha()
        }
        resp = self.session.post('https://www.zhihu.com/login/phone_num', data, headers=self.headers).content
        cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
        for cookie in cookies:
            self.cookies[cookie] = cookies[cookie]

        # print(json.loads(resp)["msg"])

        return resp

    def get_follower_list(self, url):
        if url is not None:
            if bloom.__contains__(url):
                print 'url is fetched'
                return
            bloom.add(url)
            # self.get_photo(url)
            url = followees_page + url[url.rindex('/') + 1:] + '/followers?limit=20'
            for cookie in self.cookies:
                resp = requests.get(url, cookies={cookie: self.cookies[cookie]}, headers=self.headers)
                if resp.status_code == 200:
                    self.cookie[cookie] = self.cookies[cookie]
                    break
            if resp.status_code != 200:
                return
            if resp is not None:
                try:
                    obj = json.loads(resp.text)
                    follower_count = obj['paging']['totals']
                except:
                    print 'resp to json error'
            if follower_count is not None and follower_count / 20 > 0:
                query_count = follower_count / 20
                while query_count > 0:
                    url = url + '&offset=' + str(20*query_count)
                    query_count = query_count - 1
                    self.set_followers(url)

    def save_user(self, user):
        try:
            sql = "insert into zh_user (avatar_url,avatar_url_template,gender,headline,`id`,is_advertiser,`name`,`type`,url,url_token,user_type) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            mysql.insertOne(sql, [user['avatar_url'], user['avatar_url_template'], user['gender'], user['headline'],
                                  user['id'], user['is_advertiser'], user['name'], user['type'], user['url'],
                                  user['url_token'], user['user_type']])
            mysql.end('commit')
        except Exception, e:
            print e

    def save_list(self):
        try:
            lists = []
            for url in self.rList:
                lists.append([url])
            print lists

            sql = "insert into python_prelist (listurl) values(%s)"
            mysql.insertMany(sql, lists)
            mysql.end('commit')
            self.rList = []
        except Exception, e:
            print e

    def set_followers(self, url):
        resp = requests.get(url, cookies=self.cookie, headers=self.headers)
        if resp.status_code != 200:
            return
        obj = json.loads(resp.text)
        data_list = obj['data']
        # if len(data_list) > 0:
        #     self.save_user(data_list)

        for data in data_list:
            self.save_user(data)
            name = data['url_token']
            _url = person_url + name
            if _url not in self.rList:
                if len(self.rList) >= 20000:
                    self.save_list()
                self.rList.append(_url)

                # for link in resp.links:
                #     print link
                # print resp.content
                # ##
                # following_name_list = BeautifulSoup(resp.text, 'lxml')\
                #     .find_all("a", class_="UserLink-link", target="_blank")
                # for name in following_name_list:
                #     _url = zhihu_url + name['href'] + '/'
                #     if _url not in self.rList:
                #         self.rList.append(_url)
                # print name['href']

    def get_photo(self, url):
        try:
            photo_url = BeautifulSoup(self.session.get(url, headers=self.headers).content, 'lxml')\
                .find('img', class_='Avatar Avatar--large UserAvatar-inner')['src']
            self.save_photo(photo_url)
        except Exception, e:
            print(url + '  get photo error')

    def save_photo(self, url):
        if url is not None:
            try:
                photo = self.session.get(url, headers=self.headers).content
                path = 'd://python_fpic/' + url[url.rindex('/') + 1:]
                if not os.path.exists('d://python_fpic/'):
                    os.makedirs('d://python_fpic/')
                if os.path.exists(path):
                    return
                with open(path, 'wb') as fb:
                    fb.write(photo)
                    fb.flush
            except:
                print url + '  save photo error'

    def get_list_from_db(self):
        pass

    def startup(self, name):
        self.get_follower_list(person_url + name)
        while len(self.rList) > 0:
            url = self.rList.pop(-1)
            print 'already url' + str(len(self.rList))
            self.get_follower_list(url)
            if len(self.rList) <= 0:
                self.get_list_from_db()


if __name__ == "__main__":
    bloom = BloomFilter(capacity=10000000, error_rate=0.0001)
    mysql = Mysql()
    followees_page = 'https://www.zhihu.com/api/v4/members/'
    person_url = 'https://www.zhihu.com/people/'
    # print search_url[:search_url.rindex('/')+1]
    zhihu = ZhiHu()
    zhihu.login('17621200065', 'ak325504')
    zhihu.startup('yang-chao-5-35')
    # zhihu.get_photo(search_url)
    # zhihu.get_followings(search_url)
    # zhihu.get_page("https://www.zhihu.com/")
    # s = raw_input("please input a string↓\n")
    # print s
