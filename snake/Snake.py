# -*- coding: utf-8 -*-
import copy
import pygame


class Snake(object):

    def __init__(self):
        self.pos_list = [[20, 16]]
        self.direction = 'R'

    def set_list(self):
        return self.pos_list

    def change_direction(self, direction):
        self.direction = direction

    def move_direction(self):
        body_length = len(self.pos_list) - 1
        while body_length > 0:
            self.pos_list[body_length] = copy.deepcopy(self.pos_list[body_length - 1])
            body_length -= 1
        if self.direction == 'R':
            self.pos_list[0][0] += 20
        elif self.direction == 'L':
            self.pos_list[0][0] -= 20
        elif self.direction == 'U':
            self.pos_list[0][1] -= 20
        elif self.direction == 'D':
            self.pos_list[0][1] += 20

    def eat_food(self, food_point):
        self.pos_list.insert(0, food_point)

if __name__ == '__main__':
    snake = Snake()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

