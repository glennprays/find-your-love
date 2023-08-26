from pygame.locals import *
from pgzero.actor import Actor
from pgzero.loaders import sounds
import pygame
from pgzero import clock
import math
import pygame.freetype

TILE_SIZE = 32
ROWS = 20
COLS = 20

WIDTH = ROWS * TILE_SIZE
HEIGHT = COLS * TILE_SIZE

MID_POS = TILE_SIZE/2

# for pausing game
paused = False

# 0 = way
# 1 = wall
# mimi = main character
# tata = target character
# enemy1 = enemy that move horizontal
# enemy2 = enemy that move vertical
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, "tata"],
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, "enemy2", 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, "enemy1", 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, "mimi", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

mimi = Actor("mimi")
tata = Actor("tata")
enemy1 = Actor("jostrip")
enemy1_direction = ["up"]
enemy2 = Actor("jimot")
enemy2_direction = ["right"]

# default Actor position
for row in range(len(maze)):
    for col in range(len(maze[row])):
        current = maze[row][col]
        pos = (col * TILE_SIZE)+MID_POS, (row * TILE_SIZE)+MID_POS
        if current == "mimi":
            mimi.pos = pos
        if current == "tata":
            tata.pos = pos
        if current == "enemy1":
            enemy1.pos = pos
        if current == "enemy2":
            enemy2.pos = pos


def draw():
    # winning checking
    if mimi.distance_to(tata) == 0:
        game_win()
    # game over checking
    elif enemy1.distance_to(mimi) == 0 or enemy2.distance_to(mimi) == 0:
        gameover()
    else:
        screen.clear()
        screen.fill((70, 30, 50))
        draw_map()
        tata.draw()
        mimi.draw()
        enemy1.draw()
        enemy2.draw()

def draw_map():
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            current = maze[row][col]
            current_x = TILE_SIZE * col
            current_y = TILE_SIZE * row
            if current == 1:
                screen.blit("dirt_block", (current_x, current_y))

def on_key_down(key):
    # checking curren position
    row = math.floor((mimi.y / TILE_SIZE))
    column = math.floor((mimi.x / TILE_SIZE))
    if key == keys.LEFT and column > 0:
        column -= 1
    elif key == keys.RIGHT and column < COLS-1:
        column += 1
    elif key == keys.UP and row > 0:
        row -= 1
    elif key == keys.DOWN and row < ROWS-1:
        row += 1
    
    move_actor(mimi, row, column)

def update():
    if paused:
        return
    
    enemy_move(enemy1, enemy1_direction)
    enemy_move(enemy2, enemy2_direction)

def move_actor(actor, row, column):
    # row and col start from 0 to n-1
    # calculate target x and y position
    X_POS = (column * TILE_SIZE) + MID_POS
    Y_POS = (row * TILE_SIZE) + MID_POS

    # prevent out of screen and wall checking
    if X_POS >= 0 and X_POS <= WIDTH and Y_POS > 0 and Y_POS <= HEIGHT and maze[row][column] != 1:
        actor.pos = X_POS, Y_POS

def game_win():
    global paused
    paused = True
    text_x = (WIDTH / 3) + 10
    text_y = HEIGHT / 3
    text_z = WIDTH / 2 - 175
    text_k = HEIGHT / 2

    screen.fill((0, 0, 0))  # make black backgroud
    screen.draw.text(
        "You Win!", (text_x, text_y), color=(255, 255, 255), fontsize=75
    )
    screen.draw.text(
        "Thank you for helping Mimi find tata",
        (text_z, text_k),
        color=(255, 255, 255),
        fontsize=30,
    )
    

def gameover():
    global paused
    paused = True
    text_x = (WIDTH / 3)
    text_y = HEIGHT / 3
    text_z = (WIDTH / 2)-100
    text_k = HEIGHT / 2

    screen.fill((0, 0, 0))  # make black backgroud
    screen.draw.text(
        "You Lose!", (text_x, text_y), color=(255, 255, 255), fontsize=75
    )
    screen.draw.text(
        "Got caught by enemy",
        (text_z, text_k),
        color=(255, 255, 255),
        fontsize=30,
    )

def enemy_move(enemy, direction):
    # this enemy move verticaly
    row = math.floor((enemy.y / TILE_SIZE))
    column = math.floor((enemy.x / TILE_SIZE))
    velocity = 1
    if direction[0] == "up":
        next = maze[row-1][column]
        if next != 1:
            enemy.y -= velocity
        elif next == 1:
            direction[0] = "down"
    elif direction[0] == "down":
        next = maze[row+1][column]
        if next != 1:
            enemy.y += velocity
        elif next == 1:
            direction[0] = "up"
    elif direction[0] == "right":
        next = maze[row][column+1]
        if next != 1:
            enemy.x += velocity
        elif next == 1:
            direction[0] = "left"
    elif direction[0] == "left":
        next = maze[row][column-1]
        if next != 1:
            enemy.x -= velocity
        elif next == 1:
            direction[0] = "right"