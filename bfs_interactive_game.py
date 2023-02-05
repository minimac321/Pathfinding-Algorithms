from collections import deque
from typing import List, Dict

# Imports
import numpy as np
import pygame as pg

from graph_utils import get_rectangular_coords, get_next_nodes_without_weight

BLOCKAGE_PROB = 0.2
TOTAL_COLS, TOTAL_ROWS = 30, 30
TILE_SIZE = 25


def init_graph(probability_grid: list) -> dict:
    # dict of adjacency lists
    graph = {}
    for y, row in enumerate(probability_grid):
        for x, col in enumerate(row):
            if not col:
                graph[(x, y)] = graph.get((x, y), []) + get_next_nodes_without_weight(
                    grid=probability_grid, x=x, y=y, total_cols=TOTAL_COLS, total_rows=TOTAL_ROWS
                )

    return graph


def init_components() -> tuple[pg.Surface, List, Dict]:
    # Create display
    pg.init()
    screen = pg.display.set_mode(size=[TOTAL_COLS * TILE_SIZE, TOTAL_ROWS * TILE_SIZE])

    # Create grid
    probability_grid = [
        np.random.choice(a=[0, 1], size=TOTAL_COLS, p=[1-BLOCKAGE_PROB, BLOCKAGE_PROB]).tolist()
        for _ in range(TOTAL_ROWS)
    ]

    graph = init_graph(probability_grid)

    return screen, probability_grid, graph


def draw_nodes(screen: pg.Surface, visited, color: pg.Color, width: int = 0, border_radius: int = -1):
    for x, y in visited:
        pg.draw.rect(surface=screen, color=color, rect=get_rectangular_coords(x, y, tile_size=TILE_SIZE), width=width,
                     border_radius=border_radius)


def update_display_with_end_node_path(screen: pg.Surface, grid: list, final_node_path):
    # fill screen and then draw grid
    screen.fill(pg.Color('black'))
    [
        [
            pg.draw.rect(
                screen,
                pg.Color('darkorange'),
                get_rectangular_coords(x, y, tile_size=TILE_SIZE), border_radius=TILE_SIZE // 5)
            for x, col in enumerate(row) if col
        ]
        for y, row in enumerate(grid)
    ]

    draw_nodes(screen, final_node_path, color=pg.Color("blue"))


def update_nodes_on_display(screen: pg.Surface, grid: list, visited: dict, queue: deque):
    # fill screen and then draw grid
    screen.fill(pg.Color('black'))
    [
        [
            pg.draw.rect(
                screen,
                pg.Color('darkorange'),
                get_rectangular_coords(x, y, tile_size=TILE_SIZE), border_radius=TILE_SIZE // 5)
            for x, col in enumerate(row) if col
        ]
        for y, row in enumerate(grid)
    ]

    # draw BFS work
    draw_nodes(screen, visited, color=pg.Color('forestgreen'))
    draw_nodes(screen, queue, color=pg.Color('darkslategray'))


def update_path_on_display(screen, cur_node, start_node, end_node, visited):
    path_head, path_segment = cur_node, cur_node
    while path_segment:
        draw_nodes(screen=screen, visited=[path_segment], color=pg.Color('white'),
                   width=TILE_SIZE, border_radius=TILE_SIZE // 3)

        path_segment = visited[path_segment]

    draw_nodes(screen=screen, visited=[start_node], color=pg.Color('blue'),
               width=TILE_SIZE, border_radius=TILE_SIZE // 3)
    draw_nodes(screen=screen, visited=[end_node], color=pg.Color('red'), width=TILE_SIZE, border_radius=TILE_SIZE // 3)
    draw_nodes(screen=screen, visited=[path_head], color=pg.Color('magenta'),
               width=TILE_SIZE, border_radius=TILE_SIZE // 3)


def get_final_path(visited: Dict, end_node: tuple[int, int]) -> dict:
    best_path_nodes = {}
    path_head, path_segment = end_node, end_node

    while True:
        next_path_segment = visited[path_segment]

        if next_path_segment is None:
            break

        best_path_nodes[path_segment] = next_path_segment
        path_segment = next_path_segment

    return best_path_nodes


def bfs(graph: dict, start_node: tuple[int, int], goal_node: tuple[int, int]):
    queue = deque([start_node])
    visited = {start_node: None}

    while queue:
        curr_node = queue.popleft()
        if curr_node == goal_node:
            break

        next_nodes = graph.get(curr_node)
        if next_nodes:
            for next_node in next_nodes:
                if next_node not in visited:
                    queue.append(next_node)
                    visited[next_node] = curr_node

    return queue, visited


def get_click_mouse_pos(screen):
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = x // TILE_SIZE, y // TILE_SIZE
    pg.draw.rect(screen, pg.Color('red'), get_rectangular_coords(grid_x, grid_y, tile_size=TILE_SIZE))
    click = pg.mouse.get_pressed()
    return (grid_x, grid_y) if click[0] else False


def driver():
    screen, grid, graph = init_components()
    clock = pg.time.Clock()

    # BFS settings
    start_node = (0, 0)
    goal_node = start_node
    queue = deque([start_node])
    visited = {start_node: None}

    while True:
        # Populate visual display
        update_nodes_on_display(screen, grid, visited, queue)

        # bfs, get path to mouse click
        mouse_pos = get_click_mouse_pos(screen)
        if mouse_pos and not grid[mouse_pos[1]][mouse_pos[0]]:
            queue, visited = bfs(graph, start_node, mouse_pos)
            goal_node = mouse_pos

        final_node_path = get_final_path(visited, goal_node)

        # Draw final path on screen
        update_display_with_end_node_path(screen, grid, final_node_path=final_node_path)

        # draw path
        draw_nodes(screen=screen, visited=[start_node], color=pg.Color('blue'), width=TILE_SIZE,
                   border_radius=TILE_SIZE // 3)
        draw_nodes(screen=screen, visited=[goal_node], color=pg.Color('magenta'), width=TILE_SIZE,
                   border_radius=TILE_SIZE // 3)

        # pygame necessary lines
        [exit() for event in pg.event.get() if event.type == pg.QUIT]
        pg.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    driver()
