import json
import sys
import time
import pygame
import os

from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from board import Board


def initialising_board(_squares, _resolution, _screen):
    button_down = False
    move_up = False
    move_down = False
    move_left = False
    move_right = False
    just_out_of_tkinter_window = False
    board = Board([])
    while True:
        cell_x_size = _resolution[0] / _squares
        cell_y_size = _resolution[1] / _squares
        _screen.fill((255, 255, 255))

        board, _screen, _resolution, _squares, cell_x_size, cell_y_size, \
        just_out_of_tkinter_window, button_down, move_up, move_down, move_left, move_right = \
            check_initialisation_events(
                board, _screen, _resolution, _squares, cell_x_size, cell_y_size,
                just_out_of_tkinter_window, button_down, move_up, move_down, move_left, move_right
            )

        abs_positions = board.absolute_position(_resolution, cell_x_size, cell_y_size, _squares)
        for position in abs_positions:
            pygame.draw.rect(_screen, (0, 0, 0), position)

        draw_grid(_screen, _resolution, cell_x_size, cell_y_size)

        pygame.display.flip()


def run_simulation(board, _squares, _resolution, _screen):
    move_up = False
    move_down = False
    move_left = False
    move_right = False
    simulation_time = 0.1

    while True:
        _screen.fill((255, 255, 255))

        board, _squares, move_up, move_down, move_left, move_right, simulation_time, continue_flag = \
            check_simulation_events(board, move_up, move_down, move_left, move_right, _squares, simulation_time)

        if continue_flag is not None:
            return continue_flag

        cell_x_size = _resolution[0] / _squares
        cell_y_size = _resolution[1] / _squares

        abs_positions = board.absolute_position(_resolution, cell_x_size, cell_y_size, _squares)
        for position in abs_positions:
            pygame.draw.rect(_screen, (0, 0, 0), position)

        draw_grid(_screen, _resolution, cell_x_size, cell_y_size)

        pygame.display.flip()
        time.sleep(simulation_time)
        next(board)


def draw_grid(_screen, _resolution, cell_x_size, cell_y_size):
    for i in range(int(_resolution[0] / cell_x_size) + 1):
        pygame.draw.line(_screen, (128, 128, 128), (i * cell_x_size, 0), (i * cell_x_size, _resolution[1]))

    for i in range(int(_resolution[1] / cell_y_size) + 1):
        pygame.draw.line(_screen, (128, 128, 128), (0, i * cell_y_size), (_resolution[0], i * cell_y_size))


def check_initialisation_events(board, _screen, _resolution, _squares, cell_x_size, cell_y_size,
                                just_out_of_tkinter_window, button_down, move_up, move_down, move_left, move_right):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if just_out_of_tkinter_window:
                    just_out_of_tkinter_window = False
                    continue
                else:
                    button_down = True

            elif event.button == 3:
                mouse_pos = pygame.mouse.get_pos()
                mouse_x = mouse_pos[0] // cell_x_size
                mouse_y = mouse_pos[1] // cell_y_size

                square = (mouse_x, mouse_y)

                board -= square

            elif event.button == 4:
                _squares -= 1
                if _squares < 2:
                    _squares = 2

            elif event.button == 5:
                _squares += 1

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            button_down = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                backup_cells = board.cells
                while True:
                    run_sim_again = run_simulation(board, _squares, _resolution, _screen)
                    if not run_sim_again:
                        board = Board(backup_cells)
                        break
                    board = Board(backup_cells)

            elif event.key == pygame.K_UP:
                move_up = True

            elif event.key == pygame.K_DOWN:
                move_down = True

            elif event.key == pygame.K_LEFT:
                move_left = True

            elif event.key == pygame.K_RIGHT:
                move_right = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                move_up = False

            elif event.key == pygame.K_DOWN:
                move_down = False

            elif event.key == pygame.K_LEFT:
                move_left = False

            elif event.key == pygame.K_RIGHT:
                move_right = False

            elif event.key == pygame.K_r:
                board = Board([])

            elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                Tk().withdraw()
                filename = askopenfilename(initialdir=f"{os.getcwd()}/saved_starts",
                                           filetypes=[("Json", '*.json')])
                if filename != "":
                    with open(filename, "r") as in_json:
                        save_json = json.load(in_json)

                    _squares = save_json["squares"]
                    board = Board([tuple(cell) for cell in save_json["start_cells"]])

                just_out_of_tkinter_window = True

            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_json = {"squares": _squares, "start_cells": board.cells}
                Tk().withdraw()
                filename = asksaveasfilename(initialdir=f"{os.getcwd()}/saved_starts",
                                             filetypes=[("Json", '*.json')])
                if filename != "":
                    with open(f"{filename.replace('.json', '')}.json", "w") as out_json:
                        json.dump(save_json, out_json)

                just_out_of_tkinter_window = True

    if button_down:
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0] // cell_x_size
        mouse_y = mouse_pos[1] // cell_y_size
        square = (mouse_x, mouse_y)

        board += square

    if move_up:
        board.translate(0, -1)
        time.sleep(0.01)
    if move_down:
        board.translate(0, 1)
        time.sleep(0.01)
    if move_left:
        board.translate(-1, 0)
        time.sleep(0.01)
    if move_right:
        board.translate(1, 0)
        time.sleep(0.01)

    return board, _screen, _resolution, _squares, cell_x_size, cell_y_size, \
           just_out_of_tkinter_window, button_down, move_up, move_down, move_left, move_right


def check_simulation_events(board: Board, move_up, move_down, move_left, move_right, _squares, simulation_time):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                _squares -= 1
                if _squares < 2:
                    _squares = 2

            elif event.button == 5:
                _squares += 1

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                move_up = True

            elif event.key == pygame.K_DOWN:
                move_down = True

            elif event.key == pygame.K_LEFT:
                move_left = True

            elif event.key == pygame.K_RIGHT:
                move_right = True

            elif event.key == pygame.K_ESCAPE:
                return board, _squares, move_up, move_down, move_left, move_right, simulation_time, False

            elif event.key == pygame.K_r:
                return board, _squares, move_up, move_down, move_left, move_right, simulation_time, True

            elif event.key == pygame.K_EQUALS:
                simulation_time -= 0.01
                if simulation_time < 0.01:
                    simulation_time = 0.01

            elif event.key == pygame.K_MINUS:
                simulation_time += 0.01

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                move_up = False

            elif event.key == pygame.K_DOWN:
                move_down = False

            elif event.key == pygame.K_LEFT:
                move_left = False

            elif event.key == pygame.K_RIGHT:
                move_right = False

    if move_up:
        board.translate(0, -1)
    if move_down:
        board.translate(0, 1)
    if move_left:
        board.translate(-1, 0)
    if move_right:
        board.translate(1, 0)

    return board, _squares, move_up, move_down, move_left, move_right, simulation_time, None


if __name__ == "__main__":
    pygame.init()
    resolution = (900, 900)
    squares = 30
    screen = pygame.display.set_mode(resolution)
    initialising_board(squares, resolution, screen)
