import heapq
import time
from heapq import heappush

# Imports
import pygame as pg

from graph_utils import get_rectangular_coords, get_circle_coords
from ui_utils import update_screen_execution_time, update_screen_path_cost, update_screen_nodes_searched

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


def draw_circle_nodes(screen: pg.Surface, visited, color: pg.Color, width: int = 0, border_radius: int = -1):
    for x, y in visited:
        center, radius = get_circle_coords(x, y)
        pg.draw.circle(screen, color=color, center=center, radius=radius)


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


def manhattan_distance(curr_node, goal_node):
    x_diff = abs(curr_node[0] - goal_node[0])
    y_diff = abs(curr_node[1] - goal_node[1])

    return x_diff + y_diff


def get_shortest_a_star_path(graph, start_node, goal_node):
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
                priority = new_node_cost + manhattan_distance(neigh_node, goal_node)
                heapq.heappush(queue, (priority, neigh_node))

                heapq.heappush(queue, (new_node_cost, neigh_node))
                cost_visited[neigh_node] = new_node_cost
                visited[neigh_node] = curr_node

    path_cost = cost_visited.get(goal_node)
    if path_cost is not None:
        shortest_path = get_shortest_path_from_visited_graph(visited, goal_node)
        return shortest_path, path_cost, visited

    return None, None, None


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


def update_screen_with_all_node(screen, start_node, goal_node):
    pg.draw.circle(screen, pg.Color('black'), *get_circle_coords(*start_node, tile_size=TILE_SIZE))
    pg.draw.circle(screen, pg.Color('black'), *get_circle_coords(*goal_node, tile_size=TILE_SIZE))



def draw_rect_nodes(screen: pg.Surface, visited, color: pg.Color, width: int = 0, border_radius: int = -1):
    for x, y in visited:
        pg.draw.rect(surface=screen, color=color, rect=get_rectangular_coords(x, y), width=width,
                     border_radius=border_radius)


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
    update_screen_with_all_node(screen, start_node, goal_node)
    update_screen_path_cost(screen, path_cost=0)

    while True:

        # Mouse Click selects the goal node
        mouse_pos = get_click_mouse_pos(screen)
        if mouse_pos:
            set_screen_with_image(screen)

            goal_node = mouse_pos
            start_time = time.process_time()
            # Get A-star path
            final_node_path, path_cost, visited = get_shortest_a_star_path(
                graph=graph, start_node=start_node, goal_node=goal_node,
            )
            execution_time = time.process_time() - start_time
            update_screen_nodes_searched(screen=screen, n_nodes_visited=len(visited))
            update_screen_path_cost(screen=screen, path_cost=path_cost)
            update_screen_execution_time(screen=screen, execution_time=execution_time)

            # Draw A-star path
            draw_circle_nodes(screen, final_node_path[1:-1:], color=pg.Color("blue"))

            # Draw Start and Goal Nodes
            draw_circle_nodes(screen=screen, visited=[start_node], color=pg.Color('black'))
            draw_circle_nodes(screen=screen, visited=[goal_node], color=pg.Color('red'))


        # pygame necessary lines
        [exit() for event in pg.event.get() if event.type == pg.QUIT]
        pg.display.flip()
        clock.tick(7)


if __name__ == "__main__":
    driver()
