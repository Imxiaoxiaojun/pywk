# -*- coding:utf-8 -*-
import requests
from bs4 import  BeautifulSoup


class Test(object):
    def __init__(self):
        self.grade = 9.0

    def get_books(self, url):
        data = requests.get(url).content
        # book_list = BeautifulSoup(data, "lxml").find_all(class_="star clearfix")
        book_list = BeautifulSoup(data, "lxml").find_all(class_="item")
        for book in book_list:
            book_info = book.contents[3].contents[5]
            grade = float(book_info.contents[3].string)
            if grade >= self.grade:
                print book.contents[3].contents[1].contents[1]['title'] + "----" + str(grade)


if __name__ == "__main__":
    i = 0
    test = Test()
    while i <= 9:
        test.get_books("https://book.douban.com/top250?start="+str(i*25))
        i = i + 1
