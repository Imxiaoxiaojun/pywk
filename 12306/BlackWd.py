# -*- coding:utf-8 -*-
import threading
import sys
import json
import re
import time
from CityCode import *
import random
import urllib
import base64
requests.packages.urllib3.disable_warnings()


class BlackWd(object):
    def __init__(self):
        self.__initMyInfo = "https://kyfw.12306.cn/otn/modifyUser/initQueryUserInfo"
        self.__initMyself = "https://kyfw.12306.cn/otn/index/initMy12306"
        self.__cur_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self.__city = CityCode()
        self.__session = requests.Session()
        self.__check_order_info = "https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"
        self.__pre_dc_order_request_url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
        self.__check_user_request_url = "https://kyfw.12306.cn/otn/login/checkUser"
        self.__check_order_request_url = "https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest"
        self.__passenger_url = "https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs"
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
        self.__is_login = False
        self.__train_date = ""
        self.__back_train_date = ""
        self.__ticket_dict = {}
        self.__friend_dict = {}

    def __pre_order(self):
        self.__get_friends()
        passenger = raw_input("请输入乘车人序号 \n").strip()
        try:
            passenger = int(passenger)
            passenger = self.__friend_dict[passenger]
        except:
            print "指令错误"
            return
        if passenger is None:
            print "指令错误"
            return
        # if self.__friend_dict[__passenger_dict]
        # 验证用户有效性
        # self.__session.post(self.__get_friends_pre_url, {"appid": "otn"}, verify=False)
        resp1 = self.__session.post(self.__check_user_request_url, data={"_json_att": ""}, verify=False).content
        print resp1

        # from_name = raw_input("请输入出发地名称(默认上海) \n").strip()
        # to_name = raw_input("请输入目的地名称(温州) \n").strip()
        # train_date = raw_input("请输入乘车日期(默认当前日期) \n").strip()
        self.__search_ticket()
        ticket = raw_input("请选择列车序号 \n").strip()
        try:
            ticket = int(ticket)
            ticket = self.__ticket_dict[ticket]
        except:
            print "指令错误"
            return
        if ticket is None:
            print "指令错误"
            return
        data = {
            "secretStr": urllib.unquote(ticket[0]),
            # "train_date": ticket[13],
            "train_date": self.__cur_date,
            "back_train_date": self.__cur_date,
            "tour_flag": "dc", ""  # dc-单程,fc-返程
            "purpose_codes": "ADULT",
            "query_from_station_name": self.__city.get_city_name(ticket[6]),
            "query_to_station_name": self.__city.get_city_name(ticket[7])
        }
        resp2 = self.__session.post(self.__check_order_request_url, data=data, verify=False).content
        # print resp2
        resp3 = self.__session.post(self.__pre_dc_order_request_url, verify=False).content
        # print resp3
        reg = re.compile(r"orderRequestDTO=(.*)")
        order_request_dto = reg.findall(resp3)
        if order_request_dto is not None:
            try:
                order_request_dto = order_request_dto[0].replace("\'", "\"")[:-1]
                order_request_dto = json.loads(order_request_dto)
            except Exception, e:
                print e
                print order_request_dto
                return
        print order_request_dto

        reg = re.compile(r"ticketInfoForPassengerForm=(.*)")
        passenger_form = reg.findall(resp3)
        if passenger_form is not None:
            try:
                passenger_form = passenger_form[0].replace("\'", "\"")[:-1]
                passenger_form = json.loads(passenger_form)
            except Exception, e:
                print e
                print passenger_form
                return
        print passenger_form['limitBuySeatTicketDTO']   # 座位类型 1-二等座
        print passenger
        data = {
            "cancel_flag": "2",
            "bed_level_order_num": "000000000000000000000000000000",
            "passengerTicketStr": "",
            "oldPassengerStr": "",
            "tour_flag": "",
            "randCode": ""

            # cancel_flag:2
            # bed_level_order_num:000000000000000000000000000000
            # 座位编号,0,票类型,乘客名,证件类型,证件号,手机号码,保存常用联系人(Y或N)
            # passengerTicketStr:1,0,1,朱亚军,1,330329199104090554,15022515510,N
            # oldPassengerStr:朱亚军,1,330329199104090554,1_
            # tour_flag:dc
        }

    def __get_captcha(self):
        data = self.__session.get(self.__captcha_url, verify=False).content
        with open('captcha.gif', 'wb') as fb:
            fb.write(data)
            fb.flush
            fb.close

    def __check_captcha(self):
        self.__get_captcha()
        while True:
            indexs = raw_input("请输入验证码代码 \n")
            if indexs.strip() != "":
                index_list = re.split(",", indexs)
                answer = ""
                for num in index_list:
                    answer = answer + str(self.__captcha_index[(int(num) - 1) * 2]) + "," + str(
                        self.__captcha_index[(int(num) - 1) * 2 + 1]) + ","
                data = {
                    "answer": answer[:-1],
                    "login_site": "E",
                    "rand": "sjrand"
                }
                resp = self.__session.post(self.__captcha_check_url, data, verify=False).content
                if resp is None:
                    print "验证码错误,系统异常"
                    self.__get_captcha()
                data = json.loads(resp)
                if data.get("result_code") != "4":
                    print json.loads(resp).get("result_message")
                    self.__get_captcha()
                else:
                    print "验证码校验成功"
                    return

    def __login(self):
        while True:
            user_name = raw_input("请输入用户名 \n")
            pass_word = raw_input("请输入密码 \n")
            if user_name.strip() != "" and pass_word.strip() != "":
                data = {
                    # "username": "337433736@qq.com",
                    # "password": "zhuyajun0409",
                      "username": "15122039381",
                      "password": "zhangguangfu985663607",
                    #   "username": user_name,
                    #   "password": pass_word,
                    #
                    "appid": "otn"
                }
                self.__check_captcha()
                resp = self.__session.post(self.__login_url, data, verify=False).content
                if resp is None:
                    print "登录失败，系统错误!"
                data = json.loads(resp)
                if not str(data.get("result_code")).strip().startswith('0'):
                    print data.get("result_message")
                else:
                    print "登录成功"
                    self.__is_login = True
                    return
            else:
                print "用户名和密码不能为空！"

    def __search_ticket(self):
        _from = raw_input("请输入起始站(默认上海) \n").strip()
        _to = raw_input("请输入终点站(默认温州) \n").strip()
        _train_date = raw_input("请输入乘车日期(默认当前日期"+self.__cur_date+")" "\n ").strip()
        _from = u"上海" if _from == "" else _from
        _to = u"温州" if _to == "" else _to
        _train_date = self.__cur_date if _train_date == "" else _train_date
        if _from.strip() != "" and _to.strip() != "" and _train_date.strip() != "":
            try:
                from_code = self.__city.get_city_code(_from.strip())
                if from_code == "":
                    print "出发地名称错误"
                    return
                to_code = self.__city.get_city_code(_to.strip())
                if to_code == "":
                    print "目的地名称错误"
                    return

                # https://kyfw.12306.cn/otn/leftTicket/log?leftTicketDTO.train_date=
                # 2017-11-15&leftTicketDTO.from_station=SHH&leftTicketDTO.to_station=RZH&purpose_codes=ADULT

                # https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2017-11-15&
                # leftTicketDTO.from_station=SHH&leftTicketDTO.to_station=RZH&purpose_codes=ADULT
                # purpose_codes旅客编码：成人为ADULT, 学生为:0X00
                url = self.__search_url + "leftTicketDTO.train_date=" + _train_date + "&leftTicketDTO.from_station=" \
                    + from_code + "&leftTicketDTO.to_station=" + to_code + "&purpose_codes=ADULT"
                data = requests.get(url, verify=False).content
                resp = json.loads(data)
                if not resp["status"]:
                    url = self.__search_url2 + "leftTicketDTO.train_date=" + _train_date + "&leftTicketDTO.from_station=" \
                        + from_code + "&leftTicketDTO.to_station=" + to_code + "&purpose_codes=ADULT"
                    data = requests.get(url, verify=False).content
                self.__get_ticket_list(data)
            except Exception, e:
                print "系统错误", e

    def __get_ticket_list(self, resp):
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
        print "序号 |车次(状态) |起始站 |终点站 |出发站 |到达站 |出发时间 |到达时间 |用时 |特等座 |一等座 |二等座 |高级软卧 |软卧 |动卧 |硬卧 |硬座 |无座"
        index = 0
        self.__ticket_dict.clear()
        for ticket in tickets:
            index = index+1
            ticket_array = re.split("\|", ticket)
            self.__ticket_dict[index] = ticket_array
            status = "(有票)"
            if ticket_array[0].strip() == "":
                status = "(无票)"
            print index, "|", str(ticket_array[3])+status, " |", self.__city.get_city_name(ticket_array[4]), " |", \
                self.__city.get_city_name(ticket_array[5]), "|", self.__city.get_city_name(
                ticket_array[6]), " |", \
                self.__city.get_city_name(ticket_array[7]), " |", ticket_array[8], " |", ticket_array[9], " |", \
                ticket_array[10], " |", ticket_array[32], " |", ticket_array[31], " |", ticket_array[30], " |", \
                ticket_array[21], " |", ticket_array[23], " |", ticket_array[33], " |", ticket_array[28], " |", \
                ticket_array[29], " |", ticket_array[26], " |"

    # 获取联系人
    def __get_friends(self):
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
            index = 0
            for friend in json.loads(friends[:-1]):
                index = index + 1
                self.__friend_dict[index] = friend
                print "序号| 姓名| 证件类型| 证件号码| 手机号码| 旅客类型"
                print index, "|", friend["passenger_name"], "|", friend["passenger_id_type_name"], "|", friend[
                    "passenger_id_no"], \
                    "|", friend["mobile_no"], "|", friend["passenger_type_name"]
        except Exception, e:
            print e

    def main(self):
        while True:
            print "-------------"
            print "1-余票查询"
            if not self.__is_login:
                print "2-登陆"
            else:
                print "3-切换用户"
                print "4-查看联系人列表"
                print "5-购票"
            print "0-退出"
            command = raw_input("请输入代码 \n")
            if command == "0":
                sys.exit()
            elif command == "1":
                self.__search_ticket()
            elif not self.__is_login and command == "2":
                self.__login()
            elif self.__is_login and command == "4":
                self.__get_friends()
            elif self.__is_login and command == "5":
                self.__pre_order()


if __name__ == "__main__":
    # str = "wdtmygdMlCq87V5SFJkr5HWUfeWJ8rLHQuOXHWDFSQmwqwxPKbkwTV6jVRMc4Yzn0y607WSPWQFV%0An%2FQhOerGByY%2BPmzmMz8g5GMjvcUGFSTvXFPy4%2B5x4Iv6fH0Vcg8dRb%2BxUyIXOgq5UwgPbL6j%2Fu2f%0AGX37eST16fxztZ22ayZqjIEuLuhMCYS8G%2BpWegUUfd%2F5L5Onq6ZaDlL9c6QRgpU3fRtDdPUiCY9z%0AdXxuL2CfB6B%2F8fFPfg%3D%3D"
    # print urllib.unquote(str)
    top = BlackWd()
    top.main()
    # cur_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    # _train_date = raw_input("请输入乘车日期(默认当前日期" + cur_date + ")" "\n ")
    # print json.dump("{name:aa,age:1}")


