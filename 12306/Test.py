# -*- coding:utf-8 -*-
import threading


class Test(threading.Thread):
    def __init__(self):
       threading.Thread.__init__(self)

    def run(self):
        while True:
            print 1


if __name__ == "__main__":
    test = Test()


