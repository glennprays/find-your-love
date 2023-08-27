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

MID_POS = TILE_SIZE / 2

# win or lose check
lose = False
win = False

def calculate_coordinate(row, column):
    x = column * TILE_SIZE
    y = row * TILE_SIZE
    return x, y


def set_game():
    global lose, win
    win = False
    lose = False
    # set default Actor position
    enemy_count = 1
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            current = maze[row][col]
            pos = (col * TILE_SIZE) + MID_POS, (row * TILE_SIZE) + MID_POS
            if current == "mimi":
                mimi.pos = pos
            elif current == "tata":
                tata.pos = pos
            elif current == "enemy":
                name = "enemy_" + str(enemy_count)
                enemy = Actor(name)
                pos = calculate_coordinate(row, col)
                enemy.x = pos[0] + MID_POS
                enemy.y = pos[1] + MID_POS
                enemies[name]["actor"] = enemy
                enemy_count += 1


"""
0 (way)
1 (wall)
mimi (main character)
tata (target character)
enemy (enemy that move horizontal and vertical)
"""
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
    "enemy_1": {"direction": ["left"], "velocity": 1.2},
    "enemy_2": {"direction": ["right"], "velocity": 0.9},
    "enemy_3": {"direction": ["right"], "velocity": 1.8},
    "enemy_4": {"direction": ["left"], "velocity": 2.3},
    "enemy_5": {"direction": ["up"], "velocity": 1.6},
}


# text buttons with rectangle
buttons = {
    "restart": {
        "width": 150,
        "height": 50,
        "x": (WIDTH - 150) / 2 - 80,
        "y": (HEIGHT - 50) / 2 + 80,
        "text": "Restart",
        "font_size": 30,
        "text_margin_top": 15,
        "text_margin_left": 40,
        "color": (255, 255, 255),
        "bg_color": (0, 128, 0),
        "callback": set_game,
    },
    "exit": {
        "width": 150,
        "height": 50,
        "x": (WIDTH - 150) / 2 + 100,
        "y": (HEIGHT - 50) / 2 + 80,
        "text": "Exit",
        "font_size": 30,
        "text_margin_top": 15,
        "text_margin_left": 52,
        "color": (255, 255, 255),
        "bg_color": (74, 177, 255),
        "callback": exit,
    },
}


mimi = Actor("mimi")
tata = Actor("tata")
set_game()


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
        enemy["actor"].draw()


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
    elif key == keys.RIGHT and column < COLS - 1:
        column += 1
    elif key == keys.UP and row > 0:
        row -= 1
    elif key == keys.DOWN and row < ROWS - 1:
        row += 1

    move_actor(mimi, row, column)


def update():
    global win, lose
    if win or lose:
        return
    # enemy collition check
    for key, enemy in enemies.items():
        if enemy["actor"].distance_to(mimi) < TILE_SIZE: 
            sounds.hit.play()
            lose = True
            return

    # Finish
    if mimi.distance_to(tata) == 0:
        sounds.finish.play()
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
    if (
        X_POS >= 0
        and X_POS <= WIDTH
        and Y_POS > 0
        and Y_POS <= HEIGHT
        and maze[row][column] != 1
    ):
        actor.pos = X_POS, Y_POS


def draw_button(button):
    screen.draw.filled_rect(
        Rect(button["x"], button["y"], button["width"], button["height"]),
        button["bg_color"],
    )
    screen.draw.text(
        button["text"],
        (
            button["x"] + button["text_margin_left"],
            button["y"] + button["text_margin_top"],
        ),
        color=button["color"],
        fontsize=button["font_size"],
    )


def game_win():
    text_x = (WIDTH / 3) + 10
    text_y = HEIGHT / 3
    text_z = WIDTH / 2 - 175
    text_k = HEIGHT / 2

    screen.fill((0, 0, 0))  # make black backgroud
    screen.draw.text("You Win!", (text_x, text_y), color=(255, 255, 255), fontsize=75)
    screen.draw.text(
        "Thank you for helping Mimi find Tata",
        (text_z, text_k),
        color=(255, 255, 255),
        fontsize=30,
    )
    draw_button(buttons["restart"])
    draw_button(buttons["exit"])


def gameover():
    text_x = WIDTH / 3
    text_y = HEIGHT / 3
    text_z = (WIDTH / 2) - 85
    text_k = HEIGHT / 2

    screen.fill((0, 0, 0))  # make black backgroud
    screen.draw.text("You Lose!", (text_x, text_y), color=(255, 255, 255), fontsize=75)
    screen.draw.text(
        "Got caught by enemy",
        (text_z, text_k),
        color=(255, 255, 255),
        fontsize=30,
    )
    draw_button(buttons["restart"])
    draw_button(buttons["exit"])


def enemy_move(enemy, direction, velocity):
    row = math.floor((enemy.y / TILE_SIZE))
    column = math.floor((enemy.x / TILE_SIZE))

    threshold_x = calculate_coordinate(row, column)[0] + MID_POS
    threshold_y = calculate_coordinate(row, column)[1] + MID_POS

    if direction[0] == "up":
        next = maze[row - 1][column]
        enemy.y -= velocity
        if next == 1 and enemy.y <= threshold_y:
            direction[0] = "down"
    elif direction[0] == "down":
        next = maze[row + 1][column]
        enemy.y += velocity
        if next == 1 and enemy.y >= threshold_y:
            direction[0] = "up"
    elif direction[0] == "right":
        next = maze[row][column + 1]
        enemy.x += velocity
        if next == 1 and enemy.x >= threshold_x:
            direction[0] = "left"
    elif direction[0] == "left":
        next = maze[row][column - 1]
        enemy.x -= velocity
        if next == 1 and enemy.x <= threshold_x:
            direction[0] = "right"


def on_mouse_down(pos, button):
    global lose, win
    if win or lose:
        if button == mouse.LEFT:
            for key, button in buttons.items():
                if check_button_clicked(button, pos):
                    button["callback"]()
        return


def check_button_clicked(button, pos):
    return (
        button["x"] <= pos[0] <= button["x"] + button["width"]
        and button["y"] <= pos[1] <= button["y"] + button["height"]
    )
