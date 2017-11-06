# -*- coding:utf-8 -*-
import pygame
from Snake import Snake
from Food import Food
import copy


def test():
    pygame.init()
    screen = pygame.display.set_mode((600, 450), 0, 32)
    pygame.display.set_caption("Greedy Snake")

    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    direction_flag = 'R'

    while True:
        screen.fill((255, 255, 255))
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

                    # Draw the food and the snake
        # food_position = copy.deepcopy(food.food_list())
        # food_position[0] += 10
        # food_position[1] += 10
        # pygame.draw.circle(screen, (255, 0, 0), food_position, 10)
        snake_position = snake.pos_list
        for pos in snake_position:
            temp_rect = pygame.Rect(pos[0], pos[1], 20, 20)
            pygame.draw.rect(screen, (255, 0, 0), temp_rect)
        pygame.display.update()
        #
        # # 20 frame of pictures per second
        # # and move the snake
        frame_rate = clock.tick(10)
        snake.change_direction(direction_flag)
        snake.move_direction()
        #
        # # Judge whether the snake eats a food or not
        # food_position = copy.deepcopy(food.food_list())
        # snake_head = copy.deepcopy(snake.pos_list[0])
        # if direction_flag == 'R':
        #     snake_head[0] += 20
        # elif direction_flag == 'L':
        #     snake_head[0] -= 20
        # elif direction_flag == 'U':
        #     snake_head[1] -= 20
        # elif direction_flag == 'D':
        #     snake_head[1] += 20
        # if snake_head == food_position:
        #     snake.eat_food(food_position)
        #     food.update_food()
        #
        #     # Judge whether the snake gets a collision or not
        # gameover_flag = False
        # snake_position = snake.pos_list
        # snake_head = snake_position[0]
        # if direction_flag == 'R':
        #     if snake_head[0] > 417:
        #         gameover_flag = True
        # elif direction_flag == 'L':
        #     if snake_head[0] < 0:
        #         gameover_flag = True
        # elif direction_flag == 'U':
        #     if snake_head[1] < 0:
        #         gameover_flag = True
        # elif direction_flag == 'D':
        #     if snake_head[1] > 305:
        #         gameover_flag = True
        # for pos in range(1, len(snake_position) - 1):
        #     if snake_head == snake_position[pos]:
        #         gameover_flag = True
        #
        # if gameover_flag:
        #     pygame.font.init()
        #     screen.fill((100, 0, 0))
        #     font = pygame.font.SysFont("arial", 32)
        #     text = font.render("Game Over!", True, (255, 0, 0))
        #     screen.blit(text, (260, 260))
        #     pygame.display.update()
        #     while True:
        #         again_event = pygame.event.poll()
        #         if again_event.type == pygame.QUIT:
        #             exit()

if __name__ == "__main__":
    test()
