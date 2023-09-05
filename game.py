from pygame.locals import *
from pgzero.actor import Actor
from pgzero.loaders import sounds
import pygame
from pgzero import clock
import math
import pygame.freetype
import time 
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
    # enemy_count = 1
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            current = maze[row][col]
            pos = (col * TILE_SIZE) + MID_POS, (row * TILE_SIZE) + MID_POS
            if current == "mimi":
                mimi.pos = pos
            elif current == "tata":
                tata.pos = pos
            # elif current == "enemy":
            #     name = "enemy_" + str(enemy_count)
            #     enemy = Actor(name)
            #     pos = calculate_coordinate(row, col)
            #     enemy.x = pos[0] + MID_POS
            #     enemy.y = pos[1] + MID_POS
            #     enemies[name]["actor"] = enemy
            #     enemy_count += 1

def set_algorithm_bfs():
    global use_bfs
    use_bfs = True
    set_game()  # Reset the game when switching algorithms

def set_algorithm_dfs():
    global use_bfs
    use_bfs = False
    set_game()  # Reset the game when switching algorithms
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
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, "mimi", 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

enemies = {
    "enemy_1": {"direction": ["left"], "velocity": 1.2},
    "enemy_2": {"direction": ["right"], "velocity": 0.9},
    "enemy_3": {"direction": ["right"], "velocity": 1.8},
    "enemy_4": {"direction": ["left"], "velocity": 2.3},
    "enemy_5": {"direction": ["up"], "velocity": 1.6},
}
use_bfs = True

# text buttons with rectangle
buttons = {
    "restart": {
        "width": 150,
        "height": 50,
        "x": (WIDTH - 150) / 2 - 80,
        "y": (HEIGHT - 0) / 2 + 80,
        "text": "Restart",
        "font_size": 30,
        "text_margin_top": 15,
        "text_margin_left": 40,
        "color": (255, 255, 255),
        "bg_color": (74, 177, 255),
        "callback": set_game,
    },
    "exit": {
        "width": 150,
        "height": 50,
        "x": (WIDTH - 150) / 2 + 100,
        "y": (HEIGHT - 0) / 2 + 80,
        "text": "Exit",
        "font_size": 30,
        "text_margin_top": 15,
        "text_margin_left": 52,
        "color": (255, 255, 255),
        "bg_color": (74, 177, 255),
        "callback": exit,
    },
}

# Create buttons for BFS and DFS algorithms
bfs_button = {
    "width": 150,
    "height": 50,
    "x": (WIDTH - 150) / 2 - 80,
    "y": (HEIGHT - 105) / 2 + 80,
    "text": "BFS",
    "font_size": 30,
    "text_margin_top": 15,
    "text_margin_left": 50,
    "color": (255, 255, 255),
    "bg_color": (0, 128, 0),  # Use a different color for the button
}

dfs_button = {
    "width": 150,
    "height": 50,
    "x": (WIDTH - 150) / 2 + 100,
    "y": (HEIGHT - 105) / 2 + 80,
    "text": "DFS",
    "font_size": 30,
    "text_margin_top": 15,
    "text_margin_left": 52,
    "color": (255, 255, 255),
    "bg_color": (0, 128, 0),  # Use a different color for the button
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

    # Draw the algorithm switch buttons
    draw_button(bfs_button)
    draw_button(dfs_button)
    draw_button(buttons["restart"])  # Move restart button
    draw_button(buttons["exit"])  # Move exit button


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
    if key == keys.F:
        finish_game_with_dfs_nodes()


def update():
    global win, lose
    if win or lose:
        return

    if use_bfs:
        finish_game_with_bfs_nodes()  # Use BFS algorithm
    else:
        finish_game_with_dfs_nodes()  # Use DFS algorithm

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

        print(X_POS, Y_POS)


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

    screen.draw.text("You Win!", (text_x, text_y), color=(255, 255, 255), fontsize=75)
    screen.draw.text(
        "Thank you for helping Mimi find Tata",
        (text_z, text_k),
        color=(255, 255, 255),
        fontsize=30,
    )
    draw_button(buttons["restart"])
    draw_button(buttons["exit"])
    draw_button(bfs_button)
    draw_button(dfs_button)


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


# def enemy_move(enemy, direction, velocity):
#     row = math.floor((enemy.y / TILE_SIZE))
#     column = math.floor((enemy.x / TILE_SIZE))

#     threshold_x = calculate_coordinate(row, column)[0] + MID_POS
#     threshold_y = calculate_coordinate(row, column)[1] + MID_POS

#     if direction[0] == "up":
#         next = maze[row - 1][column]
#         enemy.y -= velocity
#         if next == 1 and enemy.y <= threshold_y:
#             direction[0] = "down"
#     elif direction[0] == "down":
#         next = maze[row + 1][column]
#         enemy.y += velocity
#         if next == 1 and enemy.y >= threshold_y:
#             direction[0] = "up"
#     elif direction[0] == "right":
#         next = maze[row][column + 1]
#         enemy.x += velocity
#         if next == 1 and enemy.x >= threshold_x:
#             direction[0] = "left"
#     elif direction[0] == "left":
#         next = maze[row][column - 1]
#         enemy.x -= velocity
#         if next == 1 and enemy.x <= threshold_x:
#             direction[0] = "right"


def on_mouse_down(pos, button):
    global lose, win
    if win or lose:
        if button == mouse.LEFT:
            for key, button in buttons.items():
                if check_button_clicked(button, pos):
                    button["callback"]()
            if check_button_clicked(bfs_button, pos):
                set_algorithm_bfs()  # Set algorithm to BFS
            if check_button_clicked(dfs_button, pos):
                set_algorithm_dfs()  # Set algorithm to DFS


def check_button_clicked(button, pos):
    return (
        button["x"] <= pos[0] <= button["x"] + button["width"]
        and button["y"] <= pos[1] <= button["y"] + button["height"]
    )


from collections import deque

# ... (previous code remains unchanged)

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []

def build_graph(maze):
    graph = [[None for _ in row] for row in maze]
    nodes = []

    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] != 1:
                node = Node(row, col)
                nodes.append(node)
                graph[row][col] = node

    for node in nodes:
        x, y = node.x, node.y
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] != 1:
                node.neighbors.append(graph[new_x][new_y])

    return graph

def bfs_shortest_path(graph, start, end):
    queue = deque([(start, [])])
    visited = set()

    while queue:
        node, path = queue.popleft()

        if node == end:
            return path

        if node in visited:
            continue

        visited.add(node)

        for neighbor in node.neighbors:
            queue.append((neighbor, path + [neighbor]))


def finish_game_with_bfs_nodes():
    global lose, win

    if win or lose:
        return

    # Calculate the row and column values of mimi inside this function
    mimi_row = math.floor(mimi.y / TILE_SIZE)
    mimi_col = math.floor(mimi.x / TILE_SIZE)

    # Calculate the row and column values of tata inside this function
    tata_row = math.floor(tata.y / TILE_SIZE)
    tata_col = math.floor(tata.x / TILE_SIZE)

    # Build the graph from the maze
    graph = build_graph(maze)

    # Find the nodes corresponding to mimi and tata
    mimi_node = graph[mimi_row][mimi_col]
    tata_node = graph[tata_row][tata_col]

    # Find the shortest path from mimi to tata using BFS on the graph
    shortest_path_nodes = bfs_shortest_path(graph, mimi_node, tata_node)

    if shortest_path_nodes:
        # Convert nodes to coordinates for moving mimi
        shortest_path = [(node.x, node.y) for node in shortest_path_nodes]

        for row, col in shortest_path:
            # Calculate the target position for each step
            target_x = col * TILE_SIZE + MID_POS
            target_y = row * TILE_SIZE + MID_POS

            # Calculate the step size for smooth animation
            step_x = (target_x - mimi.x) / 5  # You can adjust the number of steps
            step_y = (target_y - mimi.y) / 5

            # Move mimi in smaller steps for smoother animation
            for _ in range(5):  # Adjust the number of steps for smoother animation
                mimi.x += step_x
                mimi.y += step_y

                # Update the screen to show the current frame of animation
                screen.clear()
                screen.fill((70, 30, 50))
                draw_map()
                tata.draw()
                mimi.draw()
                pygame.display.flip()  # Update the screen

                # Control the frame rate
                clock.tick(30)  # Adjust the frame rate for smoother animation
                time.sleep(0.01)
    # Check if mimi reached tata
    if mimi_row == tata_row and mimi_col == tata_col:
        win = True

def dfs_shortest_path(graph, start, end):
    stack = [(start, [])]
    visited = set()

    while stack:
        node, path = stack.pop()

        if node == end:
            return path

        if node in visited:
            continue

        visited.add(node)

        for neighbor in node.neighbors:
            stack.append((neighbor, path + [neighbor]))

def finish_game_with_dfs_nodes():
    global lose, win

    if win or lose:
        return

    # Calculate the row and column values of mimi inside this function
    mimi_row = math.floor(mimi.y / TILE_SIZE)
    mimi_col = math.floor(mimi.x / TILE_SIZE)

    # Calculate the row and column values of tata inside this function
    tata_row = math.floor(tata.y / TILE_SIZE)
    tata_col = math.floor(tata.x / TILE_SIZE)

    # Build the graph from the maze
    graph = build_graph(maze)

    # Find the nodes corresponding to mimi and tata
    mimi_node = graph[mimi_row][mimi_col]
    tata_node = graph[tata_row][tata_col]

    # Find the shortest path from mimi to tata using DFS on the graph
    shortest_path_nodes = dfs_shortest_path(graph, mimi_node, tata_node)

    if shortest_path_nodes:
        # Convert nodes to coordinates for moving mimi
        shortest_path = [(node.x, node.y) for node in shortest_path_nodes]

        for row, col in shortest_path:
            # Calculate the target position for each step
            target_x = col * TILE_SIZE + MID_POS
            target_y = row * TILE_SIZE + MID_POS

            # Calculate the step size for smooth animation
            step_x = (target_x - mimi.x) / 5  # You can adjust the number of steps
            step_y = (target_y - mimi.y) / 5

            # Move mimi in smaller steps for smoother animation
            for _ in range(5):  # Adjust the number of steps for smoother animation
                mimi.x += step_x
                mimi.y += step_y

                # Update the screen to show the current frame of animation
                screen.clear()
                screen.fill((70, 30, 50))
                draw_map()
                tata.draw()
                mimi.draw()
                pygame.display.flip()  # Update the screen

                # Control the frame rate
                clock.tick(30)  # Adjust the frame rate for smoother animation
                time.sleep(0.01)

    # Check if mimi reached tata
    if mimi_row == tata_row and mimi_col == tata_col:
        win = True
