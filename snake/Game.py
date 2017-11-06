# -*- coding: utf-8 -*-
from Board import Board
from Snake import Snake
import pygame
import random
from Utils import Utils


class Game(object):
    board = Board()
    snake = Snake()

    def __init__(self):
        pass
        # self.new_food()
        # self.board.clear()
        # self.board.put_snake(self.snake.getPoints())
        # self.board.put_food(self.food)

    def run(self):
        while True:
            # 检测例如按键等pygame事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        direction_flag = 'R'
                    elif event.key == pygame.K_LEFT:
                        direction_flag = 'L'
                    elif event.key == pygame.K_UP:
                        direction_flag = 'U'
                    elif event.key == pygame.K_DOWN:
                        direction_flag = 'D'
            snake_position = self.snake.pos_list
            for pos in snake_position:
                snake_image = Utils.load_image('snake_head.png')
                self.board.screen.blit(snake_image, (pos[0], pos[1]))
                # pygame.draw.rect(self.self.board.screen, (255, 0, 0), temp_rect)
            pygame.display.update()
            frame_rate = pygame.time.Clock().tick(10)
            snake_head = snake_position[0]
            if snake_head[0] < 560:
                self.snake.change_direction('R')
                self.snake.move_direction()
            else:
                if snake_head[1] < 400:
                    self.snake.change_direction('D')
                    self.snake.move_direction()
            # if x < 5:
            #     x += 1
            # else:
            #     x = 0

if __name__ == '__main__':
    Game().run()
