import json
import sys
import time
import pygame
import os

from typing import Tuple, Optional, List
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from board import Board


def initialising_board(board: Board, _screen: pygame.Surface) -> None:
    button_down = False
    movement = [False, False, False, False]
    out_of_tkinter_window = False

    while True:
        _screen.fill((255, 255, 255))

        board, _screen, out_of_tkinter_window, button_down, movement = \
            check_initialisation_events(board, _screen, out_of_tkinter_window, button_down, movement)

        draw_grid(_screen, board)
        for position in abs(board):
            pygame.draw.rect(_screen, (0, 0, 0), position)

        pygame.display.flip()


def run_simulation(board: Board, _screen: pygame.Surface) -> bool:
    movement = [False, False, False, False]
    simulation_time = 0.1

    while True:
        _screen.fill((255, 255, 255))

        board, movement, simulation_time, continue_flag = check_simulation_events(board, movement, simulation_time)

        if continue_flag is not None:
            return continue_flag

        draw_grid(_screen, board)
        for position in abs(board):
            pygame.draw.rect(_screen, (0, 0, 0), position)

        pygame.display.flip()
        time.sleep(simulation_time)
        next(board)


def draw_grid(_screen: pygame.Surface, board: Board) -> None:
    for i in range(int(board.resolution[0] / board.cell_x_size) + 1):
        pygame.draw.line(_screen, (128, 128, 128),
                         (i * board.cell_x_size, 0), (i * board.cell_x_size, board.resolution[1]))

    for i in range(int(board.resolution[1] / board.cell_y_size) + 1):
        pygame.draw.line(_screen, (128, 128, 128),
                         (0, i * board.cell_y_size), (board.resolution[0], i * board.cell_y_size))


def check_initialisation_events(
        board: Board, _screen: pygame.Surface, out_of_tkinter_window: bool, button_down: bool, movement: List[bool])\
            -> Tuple[Board, pygame.Surface, bool, bool, List[bool]]:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if out_of_tkinter_window:
                    out_of_tkinter_window = False
                    continue
                else:
                    button_down = True

            elif event.button == 3:
                mouse_pos = pygame.mouse.get_pos()
                mouse_x = mouse_pos[0] // board.cell_x_size
                mouse_y = mouse_pos[1] // board.cell_y_size

                square = (mouse_x, mouse_y)

                board -= square

            elif event.button == 4:
                board.zoom(-1)

            elif event.button == 5:
                board.zoom(1)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            button_down = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                backup_cells = board.cells
                backup_res = board.resolution
                backup_squares = board.squares
                while True:
                    run_sim_again = run_simulation(board, _screen)
                    if not run_sim_again:
                        board = Board(backup_cells, backup_res, backup_squares)
                        break
                    board = Board(backup_cells, backup_res, backup_squares)

            elif event.key == pygame.K_UP:
                movement[0] = True

            elif event.key == pygame.K_DOWN:
                movement[1] = True

            elif event.key == pygame.K_LEFT:
                movement[2] = True

            elif event.key == pygame.K_RIGHT:
                movement[3] = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                movement[0] = False

            elif event.key == pygame.K_DOWN:
                movement[1] = False

            elif event.key == pygame.K_LEFT:
                movement[2] = False

            elif event.key == pygame.K_RIGHT:
                movement[3] = False

            elif event.key == pygame.K_r:
                board = Board(set(), board.resolution, board.squares)

            elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                Tk().withdraw()
                filename = askopenfilename(initialdir=f"{os.getcwd()}/saved_starts",
                                           filetypes=[("Json", '*.json')])
                if filename != "":
                    with open(filename, "r") as in_json:
                        save_json = json.load(in_json)
 
                    board = Board(set(tuple(cell) for cell in save_json["start_cells"]), resolution, save_json["squares"])

                out_of_tkinter_window = True

            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_json = {"squares": board.squares, "start_cells": board.cells}
                Tk().withdraw()
                filename = asksaveasfilename(initialdir=f"{os.getcwd()}/saved_starts",
                                             filetypes=[("Json", '*.json')])
                if filename != "":
                    with open(f"{filename.replace('.json', '')}.json", "w") as out_json:
                        json.dump(save_json, out_json)

                out_of_tkinter_window = True

    if button_down:
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0] // board.cell_x_size
        mouse_y = mouse_pos[1] // board.cell_y_size
        square = (mouse_x, mouse_y)

        board += square

    if movement[0]:
        board.translate(0, -1)
        time.sleep(0.01)
    if movement[1]:
        board.translate(0, 1)
        time.sleep(0.01)
    if movement[2]:
        board.translate(-1, 0)
        time.sleep(0.01)
    if movement[3]:
        board.translate(1, 0)
        time.sleep(0.01)

    return board, _screen, out_of_tkinter_window, button_down, movement


def check_simulation_events(
        board: Board, movement: list, simulation_time: float) -> Tuple[Board, List[bool], float, Optional[bool]]:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                board.zoom(-1)

            elif event.button == 5:
                board.zoom(1)

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                movement[0] = True

            elif event.key == pygame.K_DOWN:
                movement[1] = True

            elif event.key == pygame.K_LEFT:
                movement[2] = True

            elif event.key == pygame.K_RIGHT:
                movement[3] = True

            elif event.key == pygame.K_ESCAPE:
                return board, movement, simulation_time, False

            elif event.key == pygame.K_r:
                return board, movement, simulation_time, True

            elif event.key == pygame.K_EQUALS:
                simulation_time -= 0.01
                if simulation_time < 0.01:
                    simulation_time = 0.01

            elif event.key == pygame.K_MINUS:
                simulation_time += 0.01

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                movement[0] = False

            elif event.key == pygame.K_DOWN:
                movement[1] = False

            elif event.key == pygame.K_LEFT:
                movement[2] = False

            elif event.key == pygame.K_RIGHT:
                movement[3] = False

    if movement[0]:
        board.translate(0, -1)
    if movement[1]:
        board.translate(0, 1)
    if movement[2]:
        board.translate(-1, 0)
    if movement[3]:
        board.translate(1, 0)

    return board, movement, simulation_time, None


if __name__ == "__main__":
    pygame.init()
    resolution = (900, 900)
    squares = 30
    screen = pygame.display.set_mode(resolution)
    initialising_board(Board(set(), resolution, squares), screen)
