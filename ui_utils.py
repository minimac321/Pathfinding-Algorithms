import pygame as pg


def update_screen_path_cost(screen, path_cost=0):
    text = f"Path Cost: {path_cost}"
    pg_large_font = pg.font.SysFont('comicsans', 30)  # Font object

    text = pg_large_font.render(text, True, (0, 0, 0))  # create our text
    screen.blit(text, (10, 3))  # draw the text to the screen


def update_screen_execution_time(screen, execution_time):
    text = f"Time: {execution_time*1000:.3f}ms"
    pg_medium_font = pg.font.SysFont('comicsans', 20)  # Font object

    text = pg_medium_font.render(text, True, (0, 0, 0))  # create our text
    screen.blit(text, (10, 40))  # draw the text to the screen


def update_screen_nodes_searched(screen, n_nodes_visited):
    text = f"Nodes Searched: {n_nodes_visited}"
    pg_medium_font = pg.font.SysFont('comicsans', 20)  # Font object

    text = pg_medium_font.render(text, True, (0, 0, 0))  # create our text
    screen.blit(text, (10, 70))  # draw the text to the screen
