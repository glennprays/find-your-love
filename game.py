import heapq
from collections import deque
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

TILES = ["cost_1", "wall", "mimi", "tata", "cost_4", "cost_5", "cost_6"]


def calculate_actor_coordinate(column, row):
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
            if current == 2:
                mimi.pos = pos
            elif current == 3:
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
0 (cost 1)
1 (wall)
2 (mimi main character)
3 (tata target character)
4 (cost 4)
5 (cost 5)
6 (cost 6)
"""
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 4, 4, 4, 4, 0, 6, 1, 0, 4, 4, 5, 5, 6, 6, 5, 4, 0, 3],
    [1, 0, 1, 1, 1, 1, 1, 6, 1, 4, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 4, 1, 1, 1, 1, 1, 6, 1, 4, 1, 0, 1, 6, 1, 4, 0, 0, 4, 1],
    [1, 4, 4, 5, 6, 6, 6, 6, 5, 4, 1, 0, 1, 6, 1, 4, 1, 1, 4, 1],
    [1, 1, 1, 1, 1, 6, 1, 5, 1, 1, 1, 0, 0, 5, 0, 4, 1, 1, 5, 1],
    [1, 0, 0, 6, 0, 6, 1, 6, 1, 1, 1, 1, 1, 5, 1, 1, 1, 6, 6, 1],
    [1, 1, 1, 6, 1, 1, 1, 6, 1, 4, 4, 0, 1, 5, 0, 0, 1, 0, 1, 1],
    [1, 1, 1, 6, 1, 1, 1, 6, 1, 5, 1, 4, 1, 4, 1, 1, 1, 0, 0, 1],
    [1, 5, 6, 6, 1, 6, 6, 0, 6, 6, 1, 4, 0, 4, 1, 1, 1, 1, 0, 1],
    [1, 5, 1, 1, 1, 6, 1, 5, 1, 1, 1, 5, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 6, 6, 6, 6, 6, 1, 5, 0, 0, 1, 6, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 6, 1, 1, 1, 1, 1, 4, 1, 1, 1, 6, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 6, 1, 1, 1, 1, 1, 4, 4, 5, 6, 6, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 4, 5, 5, 6, 1],
    [1, 5, 1, 5, 1, 1, 1, 5, 5, 5, 1, 1, 0, 0, 4, 4, 5, 1, 1, 1],
    [1, 4, 5, 4, 4, 6, 1, 5, 5, 5, 1, 1, 4, 1, 1, 1, 5, 1, 1, 1],
    [1, 1, 1, 1, 1, 4, 1, 0, 1, 1, 1, 1, 4, 1, 5, 1, 6, 1, 0, 1],
    [1, 5, 5, 5, 6, 4, 4, 4, 5, 6, 6, 5, 5, 4, 4, 1, 5, 4, 0, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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

mimi = Actor(TILES[2])
tata = Actor(TILES[3])


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
            tile = 0

            if current != 2 and current != 3:
                screen.blit(TILES[current], (current_x, current_y))


def draw():
    screen.clear()

    # show menu screen
    menu_screen()


def update():
    if use_bfs:
        finish_game_with_bfs_nodes()
    elif use_dfs:
        finish_game_with_dfs_nodes()
    elif use_ucs:
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


def check_button_clicked(button, pos):
    return (
        button["x"] <= pos[0] <= button["x"] + button["width"]
        and button["y"] <= pos[1] <= button["y"] + button["height"]
    )


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


class Node:
    def __init__(self, row, col, cost):
        self.row = row
        self.col = col
        self.neighbors = []
        self.cost = cost

    def __lt__(self, other):
        if self.row != other.row:
            return self.row < other.row
        return self.col < other.col

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)


def build_tree(maze):
    tree = [[None for _ in row] for row in maze]
    nodes = []
    mimi_row, mimi_col, tata_row, tata_col = 0, 0, 0, 0

    for row in range(len(maze)):
        for col in range(len(maze[row])):
            current = maze[row][col]
            if current == 2:
                mimi_row, mimi_col = row, col

            if current == 3:
                tata_row, tata_col = row, col

            if current != 1:
                cost = 0
                if current == 0:
                    cost = 1
                elif current != 2 and current != 3:
                    cost = current
                node = Node(row, col, cost)
                nodes.append(node)
                tree[row][col] = node

    for node in nodes:
        row, col = node.row, node.col
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for d_row, d_col in directions:
            new_row, new_col = row + d_row, col + d_col
            if (
                0 <= new_row < len(maze)
                and 0 <= new_col < len(maze[0])
                and maze[new_row][new_col] != 1
            ):
                node.neighbors.append(tree[new_row][new_col])

    mimi_node = tree[mimi_row][mimi_col]
    tata_node = tree[tata_row][tata_col]

    return mimi_node, tata_node


def move_by_path(shortest_path_finder, build_tree, show_cost=False):
    mimi_node, tata_node = build_tree(maze)

    shortest_path_nodes, calculate_path = shortest_path_finder(mimi_node, tata_node)

    if shortest_path_nodes and calculate_path:
        path_list = []
        for path in calculate_path:
            path_list.append(path)
            draw_element()
            draw_path("heart_empty", path_list)
            pygame.display.flip()
            time.sleep(0.02)

        short_path_list = []
        cost = 0
        for path in shortest_path_nodes:
            cost += path.cost
            short_path_list.append(path)
            draw_element()
            draw_path("heart_empty", path_list)
            draw_path("heart_full", short_path_list)
            pygame.display.flip()
            time.sleep(0.02)

        if show_cost:
            print(f"\033[93;1mTOTAL COST:\033[0m {cost}")

        shortest_path = [(node.row, node.col) for node in shortest_path_nodes]

        for row, col in shortest_path:
            target_col, target_row = calculate_actor_coordinate(col, row)

            steps = 10
            step_x = (target_col - mimi.x) / steps
            step_y = (target_row - mimi.y) / steps

            for _ in range(steps):
                mimi.x += step_x
                mimi.y += step_y

                draw_element()
                draw_path("heart_empty", path_list)
                draw_path("heart_full", short_path_list)
                mimi.draw()
                tata.draw()
                pygame.display.flip()

                clock.tick(30)
                time.sleep(0.01)
    time.sleep(0.5)


def draw_path(type, path_list):
    for path in path_list:
        screen.blit(type, (path.col * TILE_SIZE, path.row * TILE_SIZE))


def bfs_shortest_path(start, end):
    queue = deque([(start, [])])
    visited = set()
    calculate_path = []

    while queue:
        node, path = queue.popleft()

        if node == end:
            return path, calculate_path

        if node in visited:
            continue

        visited.add(node)

        for neighbor in node.neighbors:
            if neighbor not in calculate_path:
                calculate_path.append(neighbor)
            queue.append((neighbor, path + [neighbor]))


def dfs_shortest_path(start, end):
    stack = [(start, [])]
    visited = set()
    calculate_path = []

    while stack:
        node, path = stack.pop()

        if node == end:
            return path, calculate_path

        if node in visited:
            continue

        visited.add(node)

        for neighbor in node.neighbors:
            if neighbor not in calculate_path:
                calculate_path.append(neighbor)
            stack.append((neighbor, path + [neighbor]))


def ucs_shortest_path(root, target):
    priority_queue = [(root.cost, root)]
    visited = {root: root.cost}
    parents = {}
    visited_nodes = []

    while priority_queue:
        current_cost, current_node = heapq.heappop(priority_queue)
        visited_nodes.append(current_node)

        if current_node == target:
            path = []
            while current_node:
                path.append(current_node)
                current_node = parents.get(current_node)
            return list(reversed(path)), visited_nodes

        for neighbor in current_node.neighbors:
            neighbor_cost = current_cost + neighbor.cost
            if neighbor not in visited or neighbor_cost < visited[neighbor]:
                visited[neighbor] = neighbor_cost
                parents[neighbor] = current_node
                heapq.heappush(priority_queue, (neighbor_cost, neighbor))

    return None, visited_nodes


def finish_game_with_bfs_nodes():
    global use_bfs
    move_by_path(bfs_shortest_path, build_tree)
    use_bfs = False


def finish_game_with_dfs_nodes():
    global use_dfs
    move_by_path(dfs_shortest_path, build_tree)
    use_dfs = False


def finish_game_with_ucs_nodes():
    global use_ucs
    move_by_path(ucs_shortest_path, build_tree, show_cost=True)
    use_ucs = False
