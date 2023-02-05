from typing import List, Dict

from constants import TOTAL_COLS, TOTAL_ROWS, TILE_SIZE, GRID_COSTS

import pygame as pg


def get_shortest_path_from_visited_graph(node_came_from_node: dict, start_node: tuple[int, int],
                                         goal_node: tuple[int, int]) -> list[int]:
    current_node = node_came_from_node.get(goal_node)
    shortest_path = [goal_node]

    while current_node != start_node:
        shortest_path.append(current_node)
        current_node = node_came_from_node[current_node]

    shortest_path_reversed = shortest_path + [start_node]
    shortest_path = list(reversed(shortest_path_reversed))
    return shortest_path


def init_structure_components(grid_costs: List = GRID_COSTS, total_columns: int = TOTAL_COLS,
                              total_rows: int = TOTAL_ROWS, tile_size: float = TILE_SIZE
                              ) -> tuple[pg.Surface, List, Dict]:
    pg.init()
    screen = pg.display.set_mode(size=[total_columns * tile_size, total_rows * tile_size])

    grid = [
        [int(char) for char in string]
        for string in grid_costs
    ]
    _grid = grid.copy()

    # dict of adjacency lists
    graph = {}
    for y, row in enumerate(_grid):
        for x, col in enumerate(row):
            graph[(x, y)] = graph.get((x, y), []) + get_valid_adjacent_nodes_with_weights(grid, x, y)

    return screen, grid, graph


def get_circle_coords(x: int, y: int, tile_size: int = TILE_SIZE):
    return (x * tile_size + tile_size // 2, y * tile_size + tile_size // 2), tile_size // 4


def get_rectangular_coords(x: int, y: int, tile_size: int = TILE_SIZE):
    return x * tile_size + 1, y * tile_size + 1, tile_size - 2, tile_size - 2


def get_valid_adjacent_nodes_with_weights(grid: list, x: int, y: int, total_cols: int = TOTAL_COLS,
                                          total_rows: int = TOTAL_ROWS) -> List:
    def _check_next_node(_x, _y):
        if 0 <= _x < total_cols and 0 <= _y < total_rows:
            return True
        return False


    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    adjacent_nodes = [
        (grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways
        if _check_next_node(x + dx, y + dy)
    ]

    return adjacent_nodes


def get_next_nodes_without_weight(grid: list, x: int, y: int, total_cols: int = TOTAL_COLS,
                                  total_rows: int = TOTAL_ROWS) -> List:
    def _check_next_node(_x, _y):
        if 0 <= _x < total_cols and 0 <= _y < total_rows and not grid[y][x]:
            return True
        return False

    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(x + dx, y + dy) for dx, dy in ways if _check_next_node(x + dx, y + dy)]


