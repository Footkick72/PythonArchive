import pygame
import math
import random

def get_food_position(snake):
    food_place=[random.randint(1,grid_length),random.randint(1,grid_height)]
    while food_place in snake:
        food_place=[random.randint(1,grid_length),random.randint(1,grid_height)]
    return food_place

def convert(grid_position):
    return [grid_position[0]*side_of_grid_square-side_of_grid_square/2,grid_position[1]*side_of_grid_square-side_of_grid_square/2]

def draw_screen(snake,food_place):
    screen.fill([255,255,255])
    pygame.draw.circle(screen,[0,0,255],convert(snake[0]),side_of_grid_square/2,0)
    for body in range(1,len(snake)):
        pygame.draw.circle(screen,[255,0,0],convert(snake[body]),side_of_grid_square/2,0)
    pygame.draw.circle(screen,[0,255,0],convert(food_place),side_of_grid_square/2,0)
    pygame.display.flip()

def warping(grid_position):
    if grid_position[0]<=0:
        grid_position[0]=grid_length
    if grid_position[1]<=0:
        grid_position[1]=grid_height
    if grid_position[0]>grid_length:
        grid_position[0]=1
    if grid_position[1]>grid_height:
        grid_position[1]=1
    return grid_position

def snake_move(snake):
        snake.insert(0,warping([snake[0][0]+direction[0],snake[0][1]+direction[1]]))
        global food_place
        if snake[0] in snake[1:]:
            print('you lose! you hit yourself!Your final score is',len(snake)-2)
            return False
        if food_place!=snake[0]:
            snake.pop()
            return True
        if food_place==snake[0]:
            food_place=get_food_position(snake)
            return True

pygame.init()
clock=pygame.time.Clock()
side_of_grid_square=10
grid_length=100
grid_height=100
screen=pygame.display.set_mode([grid_length*side_of_grid_square,grid_height*side_of_grid_square])
snake=[[grid_length/2,grid_height/2]]
up=[0,-1]
down=[0,+1]
left=[-1,0]
right=[+1,0]
direction=up
running=True
food_place=get_food_position(snake)

while running:
    draw_screen(snake,food_place)
    running=snake_move(snake)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                direction=up
            if event.key==pygame.K_DOWN:
                direction=down
            if event.key==pygame.K_LEFT:
                direction=left
            if event.key==pygame.K_RIGHT:
                direction=right
    clock.tick(15)
pygame.quit()
