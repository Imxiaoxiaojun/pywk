# -*- coding: utf-8 -*-
import os
import pygame
from Utils import Utils
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (500, 300)


class Board(object):
    screen_width = 600
    screen_height = 450
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    def __init__(self):
        pygame.display.set_caption('snake')
        back_image = Utils.load_image('bg.png')
        self.screen.blit(back_image, (0, 0))
        pygame.display.flip()

    def put_snake_head(self):
        snake_image = Utils.load_image('snake_head.png')
        self.board.screen.blit(snake_image, (25, 25))
        pygame.display.update()

if __name__ == '__main__':
    Board()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
