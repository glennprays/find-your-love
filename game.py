from pygame.locals import *
from pgzero.actor import Actor
from pgzero.loaders import sounds
import pygame
from pgzero import clock
import math
import pygame.freetype

TILE_SIZE = 32 
WIDTH = 20 * TILE_SIZE 
HEIGHT = 20 * TILE_SIZE 

START_POS_X = 1 * TILE_SIZE
START_POS_Y = 19 * TILE_SIZE

END_POS_X = 19 * TILE_SIZE
END_POS_Y = 1 * TILE_SIZE

MID_POS = 16.5
mimi = Actor('mimi')
mimi.pos = START_POS_X+MID_POS,START_POS_Y+MID_POS
tata = Actor('tata')
tata.pos = END_POS_X+MID_POS,END_POS_Y+MID_POS

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
] 

win = False

def draw():
    text_x = WIDTH / 3 + 10
    text_y = HEIGHT / 3
    text_z = WIDTH / 2 - 175
    text_k = HEIGHT / 2

    if win:
        screen.fill((0, 0, 0))  # Latar belakang hitam saat pemain menang
        screen.draw.text("You Win!", (text_x, text_y), color=(255, 255, 255), fontsize=75)
        screen.draw.text("Thank you for helping Mimi found tata", (text_z, text_k), color=(255, 255, 255), fontsize=30)

    else:
        screen.clear()
        screen.fill((70, 30, 50))
        create_map()
        tata.draw()
        mimi.draw()


def create_map():
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            current = maze[row][col]
            current_x = (TILE_SIZE * col)
            current_y = (TILE_SIZE * row)
            if current == 1:
                screen.blit('dirt_block', (current_x, current_y))

def move_up():
    target = mimi.y - TILE_SIZE
    if target > 0:
        mimi.y = target
def move_down():
    target = mimi.y + TILE_SIZE
    if target < HEIGHT:
        mimi.y = target
def move_left():
    target = mimi.x - TILE_SIZE
    if target > 0:
        mimi.x = target
def move_right():
    target = mimi.x + TILE_SIZE
    if target < WIDTH:
        mimi.x = target

def update():
    global win 

    coloumn = math.floor((mimi.x / TILE_SIZE))
    row = math.floor((mimi.y / TILE_SIZE))
    # TODO: FINISH WIN GAME
    if coloumn == 19 and row == 1:
        win = True 
    
    if win:
        return
        

    elif keyboard.up and row-1 >= 0:
        if maze[row-1][coloumn] == 0:
            clock.schedule_unique(move_up,0.05)
    elif keyboard.down and row+1 < (HEIGHT/TILE_SIZE):
        if maze[row+1][coloumn] == 0:
            clock.schedule_unique(move_down,0.05)
    elif keyboard.left and coloumn-1 > 0:
        if maze[row][coloumn-1] == 0:
            clock.schedule_unique(move_left,0.05)
    elif keyboard.right and coloumn+1 < (WIDTH/TILE_SIZE):
        if maze[row][coloumn+1] == 0:
            clock.schedule_unique(move_right,0.05)
