# -*- coding:utf-8 -*-
import requests
import re
import json
from bs4 import  BeautifulSoup


class CityCode(object):
    def __init__(self):
        self.__city_txt = open('./cityCode.txt')
        self.__city_dict = {}
        self.__name_list = []
        self.__code_list = []
        self.__init_city_dict()

    def __init_city_file(self):
        self.__city_txt = open('./cityCode.txt', 'a+')
        self.__city_txt.truncate()
        url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=99"
        data = requests.get(url, verify=False).content
        city_codes = data[data.index('\'') + 2:data.rindex('\'')]
        city_code_list = re.split("@", city_codes)

        for city_code in city_code_list:
            city = re.split("\|", city_code)
            name = city[1]
            code = city[2]
            self.__name_list.append(name)
            self.__code_list.append(code)
            # self.__city_dict[name] = code
        self.__city_dict["name"] = self.__name_list
        self.__city_dict["code"] = self.__code_list
        print >> self.__city_txt, json.dumps(self.__city_dict)
        self.__city_txt.flush()
        self.__city_txt.close()

    def __init_city_dict(self):
        data = self.__city_txt.read()
        if data.strip() is None or data.strip() == "":
            print "字典为空，初始化城市代码中..."
            self.__init_city_file()
        else:
            self.__city_dict = json.loads(data)
            self.__code_list = self.__city_dict["code"]
            self.__name_list = self.__city_dict["name"]

    def get_city_code(self, name):
        if len(self.__code_list) <= 0 or len(self.__name_list) <= 0:
            print "字典为空，初始化城市代码中..."
            self.__init_city_file()
        return self.__code_list[self.__name_list.index(name)]

    def get_city_name(self, code):
        if len(self.__code_list) <= 0 or len(self.__name_list) <= 0:
            print "字典为空，初始化城市代码中..."
            self.__init_city_file()
        return self.__name_list[self.__code_list.index(code)]

if __name__ == "__main__":
    test = CityCode()
    # print test.get_city_code(u'上海')
    print test.get_city_name(u"HGH")
    print test.get_city_name(u"VRH")
    # test.init_city_code()
    # test.get_city_code()



