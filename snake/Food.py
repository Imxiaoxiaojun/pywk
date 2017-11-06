# -*- coding: utf-8 -*-
from random import *


class Food(object):

    def __init__(self):
        x = randint(4, 15) * 20
        y = randint(4, 15) * 20
        self.food_position = [x, y]

    def food_list(self):
        return self.food_position

    def update_food(self):
        self.food_position[0] = randint(0, 20) * 20
        self.food_position[1] = randint(0, 20) * 20
