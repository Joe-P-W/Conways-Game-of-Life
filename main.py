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
    start_cells = []
    while True:
        cell_x_size = _resolution[0] / _squares
        cell_y_size = _resolution[1] / _squares
        _screen.fill((255, 255, 255))

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
                    mouse_x = mouse_pos[0]//cell_x_size
                    mouse_y = mouse_pos[1]//cell_y_size

                    square = (mouse_x, mouse_y)

                    if square in start_cells:
                        start_cells.remove(square)

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
                    while True:
                        run_sim_again = run_simulation(Board(start_cells), _squares, _resolution, _screen)
                        if not run_sim_again:
                            break


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
                    start_cells = []

                elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    Tk().withdraw()
                    filename = askopenfilename(initialdir=f"{os.getcwd()}/saved_starts",
                                               filetypes=[("Json", '*.json')])
                    if filename != "":
                        with open(filename, "r") as in_json:
                            save_json = json.load(in_json)

                        _squares = save_json["squares"]
                        start_cells = [tuple(cell) for cell in save_json["start_cells"]]

                    just_out_of_tkinter_window = True

                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    save_json = {"squares": _squares, "start_cells": start_cells}
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

            if square not in set(start_cells):
                start_cells.append(square)

        if move_up:
            start_cells = [(cell[0], cell[1] - 1) for cell in start_cells]
            time.sleep(0.01)
        if move_down:
            start_cells = [(cell[0], cell[1] + 1) for cell in start_cells]
            time.sleep(0.01)
        if move_left:
            start_cells = [(cell[0] - 1, cell[1]) for cell in start_cells]
            time.sleep(0.01)
        if move_right:
            start_cells = [(cell[0] + 1, cell[1]) for cell in start_cells]
            time.sleep(0.01)

        for cell in start_cells:
            pos = ((cell[0] / _squares) * _resolution[0], (cell[1] / _squares) * _resolution[0], cell_x_size, cell_y_size)
            pygame.draw.rect(_screen, (0, 0, 0), pos)

        for i in range(int(_resolution[0] // cell_x_size) + 1):
            pygame.draw.line(_screen, (128, 128, 128), (i * cell_x_size, 0), (i * cell_x_size, _resolution[1]))

        for i in range(int(_resolution[1] // cell_y_size) + 1):
            pygame.draw.line(_screen, (128, 128, 128), (0, i * cell_y_size), (_resolution[0], i * cell_y_size))

        pygame.display.flip()


def run_simulation(board, _squares, _resolution, _screen):
    move_up = False
    move_down = False
    move_left = False
    move_right = False

    while True:
        _screen.fill((255, 255, 255))

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
                    return False

                elif event.key == pygame.K_r:
                    return True

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
            board.cells = [(cell[0], cell[1] - 1) for cell in board.cells]
            board.unoccupied_neighbours = [(cell[0], cell[1] - 1) for cell in board.unoccupied_neighbours]
        if move_down:
            board.cells = [(cell[0], cell[1] + 1) for cell in board.cells]
            board.unoccupied_neighbours = [(cell[0], cell[1] + 1) for cell in board.unoccupied_neighbours]
        if move_left:
            board.cells = [(cell[0] - 1, cell[1]) for cell in board.cells]
            board.unoccupied_neighbours = [(cell[0] - 1, cell[1]) for cell in board.unoccupied_neighbours]
        if move_right:
            board.cells = [(cell[0] + 1, cell[1]) for cell in board.cells]
            board.unoccupied_neighbours = [(cell[0] + 1, cell[1]) for cell in board.unoccupied_neighbours]

        cell_x_size = _resolution[0] / _squares
        cell_y_size = _resolution[1] / _squares

        for cell in board.cells:
            pos = ((cell[0] / _squares) * _resolution[0], (cell[1] / _squares) * _resolution[0], cell_x_size, cell_y_size)

            pygame.draw.rect(_screen, (0, 0, 0), pos)

        for i in range(int(_resolution[0] / cell_x_size) + 1):
            pygame.draw.line(_screen, (128, 128, 128), (i * cell_x_size, 0), (i * cell_x_size, _resolution[1]))

        for i in range(int(_resolution[1] / cell_y_size) + 1):
            pygame.draw.line(_screen, (128, 128, 128), (0, i * cell_y_size), (_resolution[0], i * cell_y_size))

        pygame.display.flip()
        board.update_cells()
        time.sleep(1/60)


if __name__ == "__main__":
    pygame.init()
    resolution = (900, 900)
    squares = 30
    screen = pygame.display.set_mode(resolution)
    initialising_board(squares, resolution, screen)
