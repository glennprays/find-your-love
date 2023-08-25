from pygame.locals import *
from pgzero.actor import Actor
from pgzero.loaders import sounds
import pygame
from pgzero import clock

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
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
] 


def draw():
    screen.clear()

    screen.fill((70, 30, 50))
    create_map()
    mimi.draw()
    tata.draw()

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
    
    if keyboard.up:
        clock.schedule_unique(move_up,0.05)
    elif keyboard.down:
        clock.schedule_unique(move_down,0.05)
    elif keyboard.left:
        clock.schedule_unique(move_left,0.05)
    elif keyboard.right:
        clock.schedule_unique(move_right,0.05)
