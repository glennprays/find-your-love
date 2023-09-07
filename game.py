from queue import PriorityQueue
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


def calculate_actor_coordinate(row, column):
    x = column * TILE_SIZE + MID_POS
    y = row * TILE_SIZE + MID_POS
    return x, y


def calculate_actor_row_col(actor):
    row = math.floor(actor.y / TILE_SIZE)
    col = math.floor(actor.x / TILE_SIZE)
    return row, col


def set_game():
    global lose, win
    win = False
    lose = False

    # set default Actor position
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            current = maze[row][col]
            pos = (col * TILE_SIZE) + MID_POS, (row * TILE_SIZE) + MID_POS
            if current == "mimi":
                mimi.pos = pos
            elif current == "tata":
                tata.pos = pos


use_bfs = False
use_dfs = False
use_ucs = False


def set_algorithm_bfs():
    global use_bfs
    use_bfs = True


def set_algorithm_dfs():
    global use_dfs
    use_dfs = True


def set_algorithm_ucs():
    global use_ucs
    use_ucs = True


"""
0 (way)
1 (wall)
mimi (main character)
tata (target character)
"""
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "tata"],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
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
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, "mimi", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


# text buttons with rectangle
buttons = {
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
    "bfs": {
        "width": 150,
        "height": 50,
        "x": (WIDTH - 150) / 2 - 80,
        "y": (HEIGHT - 105) / 2 + 80,
        "text": "BFS",
        "font_size": 30,
        "text_margin_top": 15,
        "text_margin_left": 50,
        "color": (255, 255, 255),
        "bg_color": (0, 128, 0),
        "callback": set_algorithm_bfs,
    },
    "dfs": {
        "width": 150,
        "height": 50,
        "x": (WIDTH - 150) / 2 + 100,
        "y": (HEIGHT - 105) / 2 + 80,
        "text": "DFS",
        "font_size": 30,
        "text_margin_top": 15,
        "text_margin_left": 52,
        "color": (255, 255, 255),
        "bg_color": (0, 128, 0),
        "callback": set_algorithm_dfs,
    },
    "ucs": {
        "width": 150,
        "height": 50,
        "x": (WIDTH - 150) / 2 - 80,
        "y": (HEIGHT - 0) / 2 + 80,
        "text": "UCS",
        "font_size": 30,
        "text_margin_top": 15,
        "text_margin_left": 50,
        "color": (255, 255, 255),
        "bg_color": (0, 128, 0),
        "callback": set_algorithm_ucs,
    },
}

mimi = Actor("mimi")
tata = Actor("tata")


def draw_element():
    screen.clear()
    screen.fill((70, 30, 50))
    draw_map()
    tata.draw()
    mimi.draw()


def draw_map():
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            current = maze[row][col]
            current_x = TILE_SIZE * col
            current_y = TILE_SIZE * row
            if current == 1:
                screen.blit("dirt_block", (current_x, current_y))


def draw():
    screen.clear()

    # show menu screen
    menu_screen()


def update():
    if use_bfs:
        print("bfs")
        finish_game_with_bfs_nodes()
    elif use_dfs:
        print("dfs")
        finish_game_with_dfs_nodes()
    elif use_ucs:
        print("ucs")
        finish_game_with_ucs_nodes()


def on_mouse_down(pos, button):
    global use_bfs, use_dfs, use_ucs
    # disable the click button whte game is running
    if use_bfs or use_dfs or use_ucs:
        return
    if button == mouse.LEFT:
        for key, button in buttons.items():
            if check_button_clicked(button, pos):
                button["callback"]()
                print("clicked", key)


def check_button_clicked(button, pos):
    return (
        button["x"] <= pos[0] <= button["x"] + button["width"]
        and button["y"] <= pos[1] <= button["y"] + button["height"]
    )


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


def menu_screen():
    # game preview as backgound
    set_game()
    draw_element()

    text_x = (WIDTH / 3) + 10
    text_y = HEIGHT / 3
    text_z = WIDTH / 2 - 175
    text_k = HEIGHT / 2

    screen.draw.text(
        "Mimi & Tata", (text_x - 35, text_y), color=(255, 255, 255), fontsize=75
    )
    screen.draw.text(
        "Help Mimi to find Tata his love",
        (text_z - 20, text_k - 50),
        color=(255, 255, 255),
        fontsize=40,
    )
    screen.draw.text(
        "Choose method:",
        (text_z + 100, text_k - 5),
        color=(255, 255, 255),
        fontsize=30,
    )
    draw_button(buttons["bfs"])
    draw_button(buttons["dfs"])
    draw_button(buttons["ucs"])
    draw_button(buttons["exit"])


from collections import deque

# ... (previous code remains unchanged)


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []


def build_tree(maze):
    tree = [[None for _ in row] for row in maze]
    nodes = []
    mimi_row, mimi_col, tata_row, tata_col = 0, 0, 0, 0

    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == "mimi":
                mimi_row, mimi_col = row, col

            if maze[row][col] == "tata":
                tata_row, tata_col = row, col

            if maze[row][col] != 1:
                node = Node(row, col)
                nodes.append(node)
                tree[row][col] = node

    for node in nodes:
        x, y = node.x, node.y
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (
                0 <= new_x < len(maze)
                and 0 <= new_y < len(maze[0])
                and maze[new_x][new_y] != 1
            ):
                node.neighbors.append(tree[new_x][new_y])

    mimi_node = tree[mimi_row][mimi_col]
    tata_node = tree[tata_row][tata_col]

    return mimi_node, tata_node


def move_by_path(shortest_path_finder, build_tree):
    mimi_node, tata_node = build_tree(maze)

    shortest_path_nodes = shortest_path_finder(mimi_node, tata_node)

    if shortest_path_nodes:
        shortest_path = [(node.x, node.y) for node in shortest_path_nodes]

        for row, col in shortest_path:
            target_x, target_y = calculate_actor_coordinate(row, col)

            steps = 10
            step_x = (target_x - mimi.x) / steps
            step_y = (target_y - mimi.y) / steps

            for _ in range(steps):
                mimi.x += step_x
                mimi.y += step_y

                draw_element()
                pygame.display.flip()

                clock.tick(30)
                time.sleep(0.01)
    time.sleep(0.5)


def draw_path(type, path_list):
    for path in path_list:
        screen.blit(type, (path.x, path.y))


def bfs_shortest_path(start, end):
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


def dfs_shortest_path(start, end):
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


def finish_game_with_bfs_nodes():
    global use_bfs
    move_by_path(bfs_shortest_path, build_tree)
    use_bfs = False


def finish_game_with_dfs_nodes():
    global use_dfs
    move_by_path(dfs_shortest_path, build_tree)
    use_dfs = False


def ucs_shortest_path(graph, start, end):
    priority_queue = PriorityQueue()
    priority_queue.put((0, start))
    visited = set()
    path = []

    while not priority_queue.empty():
        cost, node = priority_queue.get()

        if node == end:
            return path, cost

        if node in visited:
            continue

        visited.add(node)
        path.append(node)

        for neighbor, edge_cost in graph[node]:
            if neighbor not in visited:
                priority_queue.put((cost + edge_cost, neighbor))

    return [], float("inf")


def build_weighted_graph(maze):
    graph = {}
    rows = len(maze)
    cols = len(maze[0])

    for row in range(rows):
        for col in range(cols):
            if maze[row][col] != 1:
                node = (row, col)
                neighbors = []

                costs = {
                    "right": 3,
                    "left": 3,
                    "up": 5,
                    "down": 10,
                }

                directions = [
                    ("right", (0, 1)),
                    ("left", (0, -1)),
                    ("up", (-1, 0)),
                    ("down", (1, 0)),
                ]

                for direction, (dx, dy) in directions:
                    new_row, new_col = row + dx, col + dy
                    if (
                        0 <= new_row < rows
                        and 0 <= new_col < cols
                        and maze[new_row][new_col] != 1
                    ):
                        neighbors.append(((new_row, new_col), costs[direction]))

                graph[node] = neighbors

    return graph


# Inisialisasi variabel lainnya


def finish_game_with_ucs_nodes():
    global lose, win

    if win or lose:
        return

    mimi_row = math.floor(mimi.y / TILE_SIZE)
    mimi_col = math.floor(mimi.x / TILE_SIZE)

    tata_row = math.floor(tata.y / TILE_SIZE)
    tata_col = math.floor(tata.x / TILE_SIZE)

    graph = build_weighted_graph(maze)

    mimi_node = (mimi_row, mimi_col)
    tata_node = (tata_row, tata_col)

    shortest_path_nodes, shortest_path_cost = ucs_shortest_path(
        graph, mimi_node, tata_node
    )

    if shortest_path_cost != float("inf"):
        total_cost = 0

        for i in range(len(shortest_path_nodes) - 1):
            current_node = shortest_path_nodes[i]
            next_node = shortest_path_nodes[i + 1]
            edge_cost = get_edge_cost(graph, current_node, next_node)
            total_cost += edge_cost

            # Move mimi to the next node
            target_x = next_node[1] * TILE_SIZE + MID_POS
            target_y = next_node[0] * TILE_SIZE + MID_POS

            step_x = (target_x - mimi.x) / 5
            step_y = (target_y - mimi.y) / 5

            for _ in range(5):
                mimi.x += step_x
                mimi.y += step_y

                screen.clear()
                screen.fill((70, 30, 50))
                draw_map()
                tata.draw()
                mimi.draw()
                pygame.display.flip()
                time.sleep(0.01)

        print("Total cost :", total_cost)

    if mimi_row == tata_row and mimi_col == tata_col:
        win = True


def get_edge_cost(graph, node1, node2):
    for neighbor, edge_cost in graph[node1]:
        if neighbor == node2:
            return edge_cost
    return float("inf")
