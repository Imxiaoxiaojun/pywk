# -*- coding:utf-8 -*-
import requests
import re
import json
import random
import sys
from CityCode import CityCode
from bs4 import BeautifulSoup


class Test(object):
    def __init__(self):
        self.__city = CityCode()
        self.__session = requests.Session()
        self.__search_url = "https://kyfw.12306.cn/otn/leftTicket/query?"
        self.__search_url2 = "https://kyfw.12306.cn/otn/leftTicket/queryA?"
        self.__captcha_url = "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=" \
                           "login&rand=sjrand&" + str(random.randint)
        self.__captcha_check_url = "https://kyfw.12306.cn/passport/captcha/captcha-check"
        self.__login_url = "https://kyfw.12306.cn/passport/web/login"
        self.__friends_url = "https://kyfw.12306.cn/otn/passengers/init"
        self.__friends_url1 = "https://kyfw.12306.cn/otn/uamauthclient"
        self.__get_friends_pre_url = "https://kyfw.12306.cn/passport/web/auth/uamtk"
        self.__captcha_index = [24, 40, 110, 38, 177, 45, 234, 57, 63, 120, 105, 118, 173, 117, 244, 121]

    def get_captcha(self):
        data = self.__session.get(self.__captcha_url, verify=False).content
        with open('captcha.gif', 'wb') as fb:
            fb.write(data)
            fb.flush
        fb.close

    def check_captcha(self):
        indexs = raw_input("input captcha list \n")
        if indexs is None:
            return
        index_list = re.split(",", indexs)
        answer = ""
        for num in index_list:
            answer = str(self.__captcha_index[(int(num)-1)*2]) + "," + str(self.__captcha_index[(int(num)-1)*2 + 1]) + ","
        data = {
            "answer": answer[:-1],
            "login_site": "E",
            "rand": "sjrand"
        }
        resp = self.__session.post(self.__captcha_check_url, data, verify=False).content
        if resp is None:
            sys.exit()
        data = json.loads(resp)
        print data.get("result_code") == "4"
        if data.get("result_code") != "4":
            print json.loads(resp).get("result_message")
            sys.exit()

    def login(self):
        data = {
            "username": "337433736@qq.com",
            "password": "zhuyajun0409",
            "appid": "otn"
        }
        resp = self.__session.post(self.__login_url, data, verify=False).content
        if resp is None:
            sys.exit()
        data = json.loads(resp)
        if not str(data.get("result_code")).strip().startswith('0'):
            print data.get("result_message")
            sys.exit()

    def get_friends(self):
        resp = self.__session.post(self.__get_friends_pre_url, {"appid": "otn"}, verify=False).content
        if resp is None:
            sys.exit()
        data = json.loads(resp)
        if not str(data.get("result_code")).strip().startswith('0'):
            print data.get("result_message")
            sys.exit()
        h = data.get("newapptk")
        self.__session.post(self.__friends_url1, {"tk": data.get("newapptk")}, verify=False).content
        resp = self.__session.post(self.__friends_url, {"tk": data.get("newapptk")}, verify=False).content
        reg = re.compile(r"passengers=(.*)")
        result = reg.findall(resp)
        if len(result) <= 0:
            sys.exit()
        try:
            # friends = friends.decode("utf-8")
            friends = result[0].replace("\'", "\"")
            for friend in json.loads(friends[:-1]):
                print friend
        except Exception, e:
            print e

    def search_ticket(self, _from=u"上海", _to=u"温州", _train_date=u"2017-11-03"):
        if _from is None or _to is None or _train_date is None:
            return
        from_code = self.__city.get_city_code(_from)
        to_code = self.__city.get_city_code(_to)
        url = self.__search_url2 + "leftTicketDTO.train_date=" + _train_date + "&leftTicketDTO.from_station=" \
            + from_code + "&leftTicketDTO.to_station=" + to_code + "&purpose_codes=ADULT"
        data = requests.get(url, verify=False).content

        self.__format_resp(data)

    def __format_resp(self, resp):
        if resp is None:
            return
        result = json.loads(resp)
        if result.get("httpstatus") != 200:
            print "response is error"
            return
        data = result["data"]
        tickets = data["result"]
        # 车次(4) |起始站(5) |终点站(6) |出发站(7) |到达站(8) |出发时间(9) |到达时间(10) |用时(11) |特等座(33)
        # |一等座(32) |二等座（31） |高级软卧(22) |软卧(24) |动卧(34) |硬卧(29) |软座 |硬座(30) |无座(27)"
        print "车次 |起始站 |终点站 |出发站 |到达站 |出发时间 |到达时间 |用时 |特等座 |一等座 |二等座 |高级软卧 |软卧 |动卧 |硬卧 |硬座 |无座"
        for ticket in tickets:
            ticket_array = re.split("\|", ticket)
            print ticket_array[3], " |", self.__city.get_city_name(ticket_array[4]), " |", \
                self.__city.get_city_name(ticket_array[5]), "|", self.__city.get_city_name(ticket_array[6]), " |", \
                self.__city.get_city_name(ticket_array[7]), " |", ticket_array[8], " |", ticket_array[9], " |", \
                ticket_array[10], " |", ticket_array[32], " |", ticket_array[31], " |", ticket_array[30], " |", \
                ticket_array[21], " |", ticket_array[23], " |", ticket_array[33], " |", ticket_array[28], " |", \
                ticket_array[29], " |", ticket_array[26], " |"


if __name__ == "__main__":
    test = Test()
    test.get_captcha()
    test.check_captcha()
    test.login()
    test.get_friends()
    # test.login()
    # from_city = raw_input("input from city name \n")
    # to_city = raw_input("input to city name \n")
    # train_date = raw_input("input train date \n")
    # test.search_ticket(from_city.decode("utf-8"), to_city.decode("utf-8"), train_date.decode("utf-8"))
    # test.search_ticket()


