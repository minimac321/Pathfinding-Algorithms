import pygame as pg

from constants import TILE_SIZE, TOTAL_ROWS, TOTAL_COLS
from graph_utils import get_circle_coords


def draw_circle_nodes(screen: pg.Surface, visited, color: pg.Color):
    for x, y in visited:
        center, radius = get_circle_coords(x, y)
        pg.draw.circle(screen, color=color, center=center, radius=radius)


def update_screen_with_all_node(screen: pg.Surface, start_node: tuple[int, int], goal_node: tuple[int, int]):
    pg.draw.circle(screen, pg.Color('black'), *get_circle_coords(*start_node, tile_size=TILE_SIZE))
    pg.draw.circle(screen, pg.Color('black'), *get_circle_coords(*goal_node, tile_size=TILE_SIZE))


def get_click_mouse_pos():
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = x // TILE_SIZE, y // TILE_SIZE
    click = pg.mouse.get_pressed()

    if click[0]:
        return grid_x, grid_y

    return False


def set_screen_with_image(screen: pg.Surface, show_grid: bool):
    background_img = "images/img_without_grid.png"
    if show_grid:
        background_img = "images/img_with_grid.png"

    # Add background image
    background = pg.image.load(background_img).convert()
    background = pg.transform.scale(background, (TOTAL_COLS * TILE_SIZE, TOTAL_ROWS * TILE_SIZE))

    # fill screen
    screen.blit(background, (0, 0))


def update_screen_path_cost(screen: pg.Surface, path_cost: int = 0):
    text = f"Path Cost: {path_cost}"
    pg_large_font = pg.font.SysFont("comicsans", 30)  # Font object

    text = pg_large_font.render(text, True, (0, 0, 0))  # create our text
    screen.blit(text, (10, 3))  # draw the text to the screen


def update_screen_execution_time(screen: pg.Surface, execution_time: float):
    text = f"Time: {execution_time*1000:.3f}ms"
    pg_medium_font = pg.font.SysFont('comicsans', 20)  # Font object

    text = pg_medium_font.render(text, True, (0, 0, 0))  # create our text
    screen.blit(text, (10, 40))  # draw the text to the screen


def update_screen_nodes_searched(screen: pg.Surface, n_nodes_visited: int):
    text = f"Nodes Searched: {n_nodes_visited}"
    pg_medium_font = pg.font.SysFont("comicsans", 20)  # Font object

    text = pg_medium_font.render(text, True, (0, 0, 0))  # create our text
    screen.blit(text, (10, 70))  # draw the text to the screen
