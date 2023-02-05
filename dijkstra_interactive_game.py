# Adapted from https://github.com/StanislavPetrovV/Python-Dijkstra-BFS-A-star
import heapq
import time
from typing import Optional

# Imports
import pygame as pg

from graph_utils import init_structure_components, get_shortest_path_from_visited_graph
from ui_utils import update_screen_execution_time, update_screen_nodes_searched, set_screen_with_image, \
    get_click_mouse_pos, draw_circle_nodes, update_screen_with_all_node, update_screen_path_cost


def get_shortest_dijkstra_path(graph: dict, start_node: tuple[int, int], goal_node: tuple[int, int]) -> Optional[dict]:
    frontier = []
    heapq.heappush(frontier, (0, start_node))

    min_cost_to_node_so_far = {start_node: 0}
    node_came_from_node = {start_node: None}

    while frontier:
        cost_to_node, curr_node = heapq.heappop(frontier)

        if curr_node == goal_node:
            break

        adjacent_nodes = graph[curr_node]

        for neigh_cost, neigh_node in adjacent_nodes:
            new_node_cost = neigh_cost + min_cost_to_node_so_far[curr_node]

            if neigh_node not in min_cost_to_node_so_far or new_node_cost < min_cost_to_node_so_far[neigh_node]:
                heapq.heappush(frontier, (new_node_cost, neigh_node))
                min_cost_to_node_so_far[neigh_node] = new_node_cost
                node_came_from_node[neigh_node] = curr_node

    current_node = node_came_from_node.get(goal_node)
    if current_node is not None:
        shortest_path = get_shortest_path_from_visited_graph(node_came_from_node, start_node, goal_node)
        path_cost = min_cost_to_node_so_far[goal_node]

        path_dict = {
            "shortest_path": shortest_path,
            "path_cost": path_cost,
            "n_visited_nodes": len(node_came_from_node),
        }
        return path_dict

    return None


def driver(show_grid: bool = False):
    screen, grid, graph = init_structure_components()
    clock = pg.time.Clock()

    # BFS settings
    start_node = (0, 7)
    goal_node = (0, 7)  # Change to mouse click

    # Set UI
    set_screen_with_image(screen, show_grid=show_grid)
    update_screen_path_cost(screen, path_cost=0)
    update_screen_with_all_node(screen, start_node, goal_node)

    while True:
        # Mouse Click selects the goal node
        mouse_pos = get_click_mouse_pos()
        if mouse_pos:
            set_screen_with_image(screen, show_grid=show_grid)

            goal_node = mouse_pos

            start_time = time.process_time()
            # Get Dijkstra path
            path_dict = get_shortest_dijkstra_path(
                graph=graph, start_node=start_node, goal_node=goal_node
            )
            final_node_path, path_cost, n_visited_nodes = path_dict.values()
            execution_time = time.process_time() - start_time
            update_screen_execution_time(screen=screen, execution_time=execution_time)
            update_screen_nodes_searched(screen=screen, n_nodes_visited=n_visited_nodes)
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
