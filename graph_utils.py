from constants import TOTAL_COLS, TOTAL_ROWS, TILE_SIZE


def get_circle_coords(x, y):
    return (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 4


def get_rectangular_coords(x: int, y: int):
    return x * TILE_SIZE + 1, y * TILE_SIZE + 1, TILE_SIZE - 2, TILE_SIZE - 2


def get_next_nodes(grid: list, x: int, y: int):
    check_next_node = lambda x, y: True if 0 <= x < TOTAL_COLS and 0 <= y < TOTAL_ROWS and not grid[y][x] else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]


def init_graph(grid: list):
    # dict of adjacency lists
    graph = {}
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if not col:
                graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(grid, x, y)

    return graph
