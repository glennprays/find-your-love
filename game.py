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

# 0 (way)
# 1 (wall)
# mimi (main character)
# tata (target character)
# enemy1 (enemy that move horizontal)
# enemy2 (enemy that move vertical)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "tata"],
    [1, 0, 1, 1, 1, 1, 1, 0, 0, "enemy", 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, "enemy", 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, "enemy", 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, "enemy", 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, "enemy", 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, "mimi", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

enemies = {
    "enemy_1": {
        "direction": ["left"],
        "velocity": 1.2
    },
    "enemy_2": {
        "direction": ["right"],
        "velocity": 0.9
    },
    "enemy_3": {
        "direction": ["right"],
        "velocity": 1.8
    },
    "enemy_4": {
        "direction": ["left"],
        "velocity": 2.3
    },
    "enemy_5": {
        "direction": ["up"],
        "velocity": 1.6
    },
}
enemies_direction = []

mimi = Actor("mimi")
tata = Actor("tata")

def calculate_coordinate(row, column):
    x = column * TILE_SIZE
    y = row * TILE_SIZE
    return x,y

enemy_count = 1
# default Actor position
for row in range(len(maze)):
    for col in range(len(maze[row])):
        current = maze[row][col]
        pos = (col * TILE_SIZE)+MID_POS, (row * TILE_SIZE)+MID_POS
        if current == "mimi":
            mimi.pos = pos
        elif current == "tata":
            tata.pos = pos
        elif current == "enemy":
            name = "enemy_"+str(enemy_count)
            enemy = Actor(name)
            pos = calculate_coordinate(row, col)
            enemy.x = pos[0] + MID_POS
            enemy.y = pos[1] + MID_POS
            enemies[name]["actor"] = enemy
            enemy_count += 1

# win or lose check
lose = False
win = False

def draw():
    global win, lose
    if lose:
        gameover()
        return
    elif win:
        game_win()
        return
    screen.clear()
    screen.fill((70, 30, 50))
    draw_map()
    tata.draw()
    mimi.draw()
    
    for key, enemy in enemies.items():
        enemy['actor'].draw()

def draw_map():
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            current = maze[row][col]
            current_x = TILE_SIZE * col
            current_y = TILE_SIZE * row
            if current == 1:
                screen.blit("dirt_block", (current_x, current_y))

def on_key_down(key):
    global win, lose
    if win or lose:
        return
    
    # checking current position
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
    global win, lose
    if win or lose:
        return
    
    # enemy collition check
    for key, enemy in enemies.items():
        if enemy["actor"].distance_to(mimi) < TILE_SIZE:
            lose = True
            return

    # Finish
    if mimi.distance_to(tata) == 0:
        win = True
        return

    # enemy movement
    for key, enemy in enemies.items():
        enemy_move(enemy["actor"], enemy["direction"], enemy["velocity"])

def move_actor(actor, row, column):
    # row and col start from 0 to n-1

    # calculate target x and y position
    X_POS = (column * TILE_SIZE) + MID_POS
    Y_POS = (row * TILE_SIZE) + MID_POS

    # prevent out of screen and wall checking
    if X_POS >= 0 and X_POS <= WIDTH and Y_POS > 0 and Y_POS <= HEIGHT and maze[row][column] != 1:
        actor.pos = X_POS, Y_POS

def game_win():
    text_x = (WIDTH / 3) + 10
    text_y = HEIGHT / 3
    text_z = WIDTH / 2 - 175
    text_k = HEIGHT / 2

    screen.fill((0, 0, 0))  # make black backgroud
    screen.draw.text(
        "You Win!", (text_x, text_y), color=(255, 255, 255), fontsize=75
    )
    screen.draw.text(
        "Thank you for helping Mimi find Tata",
        (text_z, text_k),
        color=(255, 255, 255),
        fontsize=30,
    )
    button_width = 150
    button_height = 50
    button_x = (WIDTH - button_width) / 2 - 80
    button_y = (HEIGHT - button_height) / 2 + 80

    screen.draw.filled_rect(Rect(button_x, button_y, button_width, button_height), (0, 128, 0))
    screen.draw.text("Restart", (button_x + 40, button_y + 15), color=(255, 255, 255), fontsize=30)

    button_width = 150
    button_height = 50
    button_z = (WIDTH - button_width) / 2 + 100
    button_k = (HEIGHT - button_height) / 2 + 80

    screen.draw.filled_rect(Rect(button_z, button_k, button_width, button_height), (74, 177, 255))
    screen.draw.text("Exit", (button_z + 52, button_k + 15), color=(255, 255, 255), fontsize=30)
    

def gameover():
    text_x = (WIDTH / 3)
    text_y = HEIGHT / 3
    text_z = (WIDTH / 2)- 85
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

    button_width = 150
    button_height = 50
    button_x = (WIDTH - button_width) / 2 - 80
    button_y = (HEIGHT - button_height) / 2 + 80

    screen.draw.filled_rect(Rect(button_x, button_y, button_width, button_height), (0, 128, 0))
    screen.draw.text("Restart", (button_x + 40, button_y + 15), color=(255, 255, 255), fontsize=30)

    button_width = 150
    button_height = 50
    button_z = (WIDTH - button_width) / 2 + 100
    button_k = (HEIGHT - button_height) / 2 + 80

    screen.draw.filled_rect(Rect(button_z, button_k, button_width, button_height), (74, 177, 255))
    screen.draw.text("Exit", (button_z + 52, button_k + 15), color=(255, 255, 255), fontsize=30)


def enemy_move(enemy, direction, velocity):
    row = math.floor((enemy.y / TILE_SIZE))
    column = math.floor((enemy.x / TILE_SIZE))

    if direction[0] == "up":
        next = maze[row-1][column]
        threshold = calculate_coordinate(row, column)[1] + MID_POS
        enemy.y -= velocity
        if next == 1 and enemy.y <= threshold:
            direction[0] = "down"
    elif direction[0] == "down":
        next = maze[row+1][column]
        threshold = calculate_coordinate(row, column)[1] + MID_POS
        enemy.y += velocity
        if next == 1 and enemy.y >= threshold:
            direction[0] = "up"
    elif direction[0] == "right":
        next = maze[row][column+1]
        threshold = calculate_coordinate(row, column)[0] + MID_POS
        enemy.x += velocity
        if next == 1 and enemy.x >= threshold:
            direction[0] = "left"
    elif direction[0] == "left":
        next = maze[row][column-1]
        threshold = calculate_coordinate(row, column)[0] + MID_POS
        enemy.x -= velocity
        if next == 1 and enemy.x <= threshold:
            direction[0] = "right"

def restart_game():
    global win, lose
    win = False
    lose = False

    # Reset posisi Mimi dan Tata
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            current = maze[row][col]
            pos = (col * TILE_SIZE) + MID_POS, (row * TILE_SIZE) + MID_POS
            if current == "mimi":
                mimi.pos = pos
            elif current == "tata":
                tata.pos = pos

    # Reset posisi musuh
    enemy_count = 1
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            current = maze[row][col]
            if current == "enemy":
                name = "enemy_" + str(enemy_count)
                enemy = enemies[name]["actor"]
                pos = calculate_coordinate(row, col)
                enemy.x = pos[0] + MID_POS
                enemy.y = pos[1] + MID_POS
                enemy_count += 1

def on_mouse_down(pos, button):
    global lose, win
    if win or lose :
        if button == mouse.LEFT and check_restart_button_click(pos) == True:
            restart_game()
        elif button == mouse.LEFT and check_exit_button_click(pos) == True:
            exit()


def check_restart_button_click(pos):
    button_width2 = 150
    button_height2 = 50
    button_z = (WIDTH - button_width2) / 2 - 80
    button_k = (HEIGHT - button_height2) / 2 + 80
    
    if (
        (button_z <= pos[0] <= button_z + button_width2 and button_k <= pos[1] <= button_k + button_height2)
    ):
        return True
    else:
        return False

def check_exit_button_click(pos):
    button_width = 150
    button_height = 50
    button_z = (WIDTH - button_width) / 2 + 100
    button_k = (HEIGHT - button_height) / 2 + 80
    
    if (
        button_z <= pos[0] <= button_z + button_width and
        button_k <= pos[1] <= button_k + button_height
    ):
        return True
    else:
        return False


