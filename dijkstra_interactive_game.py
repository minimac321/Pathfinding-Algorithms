# Adapted from https://github.com/StanislavPetrovV/Python-Dijkstra-BFS-A-star
import heapq
from collections import deque
from heapq import heappush

# Imports
import pygame as pg

from graph_utils import get_rectangular_coords, get_circle_coords

"""
TODO:
- Catch edge case when the starting point is surrounded by blockages and cannot propagate
"""

TOTAL_COLS, TOTAL_ROWS = 23, 13
TILE_SIZE = 40
BLOCKAGE_PROB = 0.2
GRID = ['22222222222222222222212',
        '22222292222911112244412',
        '22444422211112911444412',
        '24444444212777771444912',
        '24444444219777771244112',
        '92444444212777791192144',
        '22229444212777779111144',
        '11111112212777772771122',
        '27722211112777772771244',
        '27722777712222772221244',
        '22292777711144429221244',
        '22922777222144422211944',
        '22222777229111111119222']


def get_next_nodes(grid: list, x: int, y: int):
    check_next_node = lambda x, y: True if 0 <= x < TOTAL_COLS and 0 <= y < TOTAL_ROWS else False

    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    adjacent_nodes = [
        (grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways
        if check_next_node(x + dx, y + dy)
    ]

    return adjacent_nodes


def draw_rect_nodes(screen: pg.Surface, visited, color: pg.Color, width: int = 0, border_radius: int = -1):
    for x, y in visited:
        pg.draw.rect(surface=screen, color=color, rect=get_rectangular_coords(x, y), width=width,
                     border_radius=border_radius)


def draw_circle_nodes(screen: pg.Surface, visited, color: pg.Color, width: int = 0, border_radius: int = -1):
    for x, y in visited:
        center, radius = get_circle_coords(x, y)
        pg.draw.circle(screen, color=color, center=center, radius=radius)


# def update_path_on_display(screen, cur_node, start_node, end_node, visited):
#     path_head, path_segment = cur_node, cur_node
#     while path_segment:
#         draw_rect_nodes(screen=screen, visited=[path_segment], color=pg.Color('white'),
#                         width=TILE_SIZE, border_radius=TILE_SIZE // 3)
#
#         # pg.draw.rect(screen, pg.Color('white'), get_rectangular_coords(*path_segment), TILE_SIZE,
#         #              border_radius=TILE_SIZE // 3)
#         path_segment = visited[path_segment]
#
#     draw_rect_nodes(screen=screen, visited=[start_node], color=pg.Color('blue'), width=TILE_SIZE,
#                     border_radius=TILE_SIZE // 3)
#     draw_rect_nodes(screen=screen, visited=[end_node], color=pg.Color('red'), width=TILE_SIZE,
#                     border_radius=TILE_SIZE // 3)
#     draw_rect_nodes(screen=screen, visited=[path_head], color=pg.Color('magenta'),
#                     width=TILE_SIZE, border_radius=TILE_SIZE // 3)


def get_final_path(graph, visited, end_node):
    best_path_nodes = {}
    path_head, path_segment = end_node, end_node

    while True:
        next_path_segment = visited[path_segment]

        if next_path_segment is None:
            break

        best_path_nodes[path_segment] = next_path_segment
        path_segment = next_path_segment

    return best_path_nodes


# Watch Tutorial: https://www.youtube.com/watch?v=bZkzH5x0SKU
def get_shortest_path_from_visited_graph(visited, goal_node):
    path = []

    curr_node = goal_node
    while curr_node:
        path.append(curr_node)
        curr_node = visited[curr_node]

    return path


def get_shortest_dijkstra_path(graph, start_node, goal_node):
    queue = []
    heappush(queue, (0, start_node))
    cost_visited = {start_node: 0}
    visited = {start_node: None}

    while queue:
        cost_to_node, curr_node = heapq.heappop(queue)

        if curr_node == goal_node:
            break

        adjacent_nodes = graph[curr_node]

        for neigh_cost, neigh_node in adjacent_nodes:
            new_node_cost = neigh_cost + cost_visited[curr_node]

            if neigh_node not in cost_visited or new_node_cost < cost_visited[neigh_node]:
                heapq.heappush(queue, (new_node_cost, neigh_node))
                cost_visited[neigh_node] = new_node_cost
                visited[neigh_node] = curr_node

    path_cost = cost_visited.get(goal_node)
    if path_cost is not None:
        shortest_path = get_shortest_path_from_visited_graph(visited, goal_node)
        return shortest_path, path_cost

    return None, None


def get_click_mouse_pos(screen):
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = x // TILE_SIZE, y // TILE_SIZE
    click = pg.mouse.get_pressed()

    if click[0]:
        return grid_x, grid_y

    return False


def init_structure_components():
    pg.init()
    screen = pg.display.set_mode(size=[TOTAL_COLS * TILE_SIZE, TOTAL_ROWS * TILE_SIZE])

    # grid from images/img_with_grid.png
    # TODO - Add a legend for terrain costs and use constants

    grid = [
        [int(char) for char in string]
        for string in GRID
    ]
    _grid = grid.copy()

    # dict of adjacency lists
    graph = {}
    for y, row in enumerate(_grid):
        for x, col in enumerate(row):
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(grid, x, y)

    return screen, grid, graph


def set_screen_with_image(screen):
    # Add background image
    background = pg.image.load('images/img_with_grid.png').convert()
    background = pg.transform.scale(background, (TOTAL_COLS * TILE_SIZE, TOTAL_ROWS * TILE_SIZE))

    # fill screen
    screen.blit(background, (0, 0))


def update_screen_with_all_node(screen, start_node, goal_node, visited):
    pg.draw.circle(screen, pg.Color('green'), *get_circle_coords(*start_node, tile_size=TILE_SIZE))
    pg.draw.circle(screen, pg.Color('black'), *get_circle_coords(*goal_node, tile_size=TILE_SIZE))

    # [
    #     pg.draw.rect(screen, pg.Color('forestgreen'), get_rectangular_coords(x, y, tile_size=TILE_SIZE), 1)
    #      for x, y in visited[1:-1:]
    # ]


def update_screen_path_cost(screen, path_cost=0):
    text = f"Path Cost: {path_cost}"
    pg_large_font = pg.font.SysFont('comicsans', 30)  # Font object

    text = pg_large_font.render(text, True, (0, 0, 0))  # create our text
    screen.blit(text, (10, 3))  # draw the text to the screen


def driver():
    screen, grid, graph = init_structure_components()
    clock = pg.time.Clock()

    # BFS settings
    start_node = (0, 7)
    goal_node = (0, 7)  # Change to mouse click
    # Create a priority queue in the form of (cost, node)
    queue = []
    heappush(queue, (0, start_node))
    visited = {start_node: None}

    # Set UI
    set_screen_with_image(screen)
    update_screen_path_cost(screen, path_cost=0)
    update_screen_with_all_node(screen, start_node, goal_node, visited)

    while True:
        # Mouse Click selects the goal node
        mouse_pos = get_click_mouse_pos(screen)
        if mouse_pos:
            set_screen_with_image(screen)

            goal_node = mouse_pos
            # Get Dijkstra path
            final_node_path, path_cost = get_shortest_dijkstra_path(
                graph=graph, start_node=start_node, goal_node=goal_node
            )

            update_screen_path_cost(screen=screen, path_cost=path_cost)

            # draw path
            draw_circle_nodes(screen=screen, visited=[start_node], color=pg.Color('black'))
            draw_circle_nodes(screen=screen, visited=[goal_node], color=pg.Color('red'))

            # Draw Dijkstra path
            draw_circle_nodes(screen, final_node_path[1:-1:], color=pg.Color("blue"))

        # pygame necessary lines
        [exit() for event in pg.event.get() if event.type == pg.QUIT]
        pg.display.flip()
        clock.tick(7)


if __name__ == "__main__":
    driver()
