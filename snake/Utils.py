# -*- coding:utf-8 -*-
import os
import pygame


class Utils(object):
    def __init__(self):
        pass

    @staticmethod
    def load_image(pic_name):
        # 获取当前脚本文件所在目录的绝对路径
        current_dir = os.path.split(os.path.abspath(__file__))[0]
        # 指定图片目录
        path = os.path.join(current_dir, 'image', pic_name)
        # 加载图片
        return pygame.image.load(path).convert()
