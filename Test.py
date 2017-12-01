# -*- coding:utf-8 -*-
import sys


class Test(object):
    def __init__(self, credit_limit=4, price=2):
        self.__price = price
        self.__bottle = 0
        self.__lid = 0
        self.__credit_limit = credit_limit
        self.__credit_used = 0
        self.__balance = 0
        self.__property = 0

    def drank(self, money):
        self.__balance = money
        count = 0
        actual_price = self.__price - self.__price / 2.0 - self.__price / 4.0
        while self.__balance != 0 or self.__credit_used != 0 or self.__property > self.__price:
            num = self.__balance / self.__price
            count = count + num

            self.__balance = self.__balance - num * self.__price
            self.__bottle = self.__bottle + num
            self.__lid = self.__lid + num

            # 2个空瓶 = 2块钱 能换多少钱计算 一个瓶子的价格的 1
            bottle_money = self.__bottle / 2 * self.__price
            self.__bottle = self.__bottle % 2

            # 4个瓶盖 = 2块钱 能换多少钱计算 一个盖子的价格0.5
            lid_money = self.__lid / 4 * self.__price
            self.__lid = self.__lid % 4

            self.__balance = self.__balance + bottle_money + lid_money
            self.__property = self.__balance - self.__credit_used + self.__lid * self.__price / 4.0 + self.__bottle * self.__price / 2.0

            # print "瓶子=", self.__bottle, "盖子=", self.__lid, "余额=", self.__balance, "count=", count
            print "瓶子=", self.__bottle, "盖子=", self.__lid, "余额=", self.__balance, "count=", \
                count, "已用额度=", self.__credit_used, "剩余额度=", self.__credit_limit

            if self.__bottle < 2 and self.__lid < 4 and self.__balance < self.__price or self.__property <= 0:
                # if self.__credit_limit >= self.__price and (self.__lid * 0.5 + self.__bottle * 1) >= self.__price:
                if self.__property >= actual_price and self.__credit_limit > 0 and self.__credit_limit >= self.__price:
                    print "开启借款模式"
                    # borrow = self.__property / self.__price * self.__price
                    # borrow = self.__credit_limit if borrow <= self.__credit_limit else int(borrow)
                    # borrow = self.__price if self.__property <= self.__credit_limit else int(self.__price)
                    borrow = int(self.__price)
                    self.__balance = self.__balance + borrow
                    self.__credit_limit = self.__credit_limit - borrow
                    self.__credit_used = self.__credit_used + borrow
                else:
                    print "超过资产额度，不能继续借，开始还款"
                    if self.__balance > 0:
                        self.__credit_used = self.__credit_used - self.__balance
                        self.__credit_limit = self.__credit_limit + self.__balance
                        self.__balance = 0
                    if self.__credit_used > 0 and self.__bottle > 0:
                        repay_count = self.__credit_used / (self.__price / 2.0)
                        repay_count = self.__bottle if repay_count > self.__bottle else repay_count
                        self.__credit_used = self.__credit_used - repay_count * self.__price / 2.0
                        self.__credit_limit = self.__credit_limit + repay_count * self.__price / 2.0
                        self.__bottle = self.__bottle - repay_count
                    if self.__credit_used > 0 and self.__lid > 0:
                        repay_count = self.__credit_used / (self.__price / 4.0)
                        repay_count = self.__lid if repay_count > self.__lid else repay_count
                        self.__credit_used = self.__credit_used - repay_count * self.__price / 4.0
                        self.__credit_limit = self.__credit_limit + repay_count * self.__price / 4.0
                        self.__lid = self.__lid - repay_count
                    if self.__credit_used != 0:
                        print "系统错误"
                        return
                    print "瓶子=", self.__bottle, "盖子=", self.__lid, "剩余资产", self.__property, \
                        "剩余额度", self.__credit_limit, "已用额度", self.__credit_used, "余额", self.__balance


if __name__ == "__main__":
    while True:
        while True:
            try:
                credit = raw_input("请输入信用额度 \n").strip()
                money1 = raw_input("请输入余额 \n").strip()
                money1 = int(money1)
                credit = int(credit)
                test = Test(credit)
                test.drank(money1)
                sys.exit()
            except Exception, e:
                print "余额必须为数字", e
