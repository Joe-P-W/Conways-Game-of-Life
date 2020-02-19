import sys
import time
import pygame

from board import Board

pygame.init()
resolution = (900, 900)
squares = 30
screen = pygame.display.set_mode(resolution)
initialising_board = True
button_down = False
start_cells = []

move_up = False
move_down = False
move_left = False
move_right = False

while initialising_board:
    cell_x_size = resolution[0] / squares
    cell_y_size = resolution[1] / squares
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                button_down = True

            elif event.button == 3:
                mouse_pos = pygame.mouse.get_pos()
                mouse_x = mouse_pos[0]//cell_x_size
                mouse_y = mouse_pos[1]//cell_y_size

                square = (mouse_x, mouse_y)

                if square in start_cells:
                    start_cells.remove(square)

            elif event.button == 4:
                squares -= 1

            elif event.button == 5:
                squares += 1

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            button_down = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                initialising_board = False

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
        pos = ((cell[0] / squares) * resolution[0], (cell[1] / squares) * resolution[0], cell_x_size, cell_y_size)
        pygame.draw.rect(screen, (0, 0, 0), pos)

    for i in range(int(resolution[0]//cell_x_size) + 1):
        pygame.draw.line(screen, (128, 128, 128), (i*cell_x_size, 0), (i*cell_x_size, resolution[1]))

    for i in range(int(resolution[1]//cell_y_size) + 1):
        pygame.draw.line(screen, (128, 128, 128), (0, i*cell_y_size), (resolution[0], i*cell_y_size))

    pygame.display.flip()


board = Board(start_cells)

while True:
    cell_x_size = resolution[0] / squares
    cell_y_size = resolution[1] / squares
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                squares -= 1

            elif event.button == 5:
                squares += 1

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
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

    for cell in board.cells:
        pos = ((cell[0] / squares) * resolution[0], (cell[1] / squares) * resolution[0], cell_x_size, cell_y_size)

        pygame.draw.rect(screen, (0, 0, 0), pos)

    for i in range(int(resolution[0]/cell_x_size) + 1):
        pygame.draw.line(screen, (128, 128, 128), (i*cell_x_size, 0), (i*cell_x_size, resolution[1]))

    for i in range(int(resolution[1]/cell_y_size) + 1):
        pygame.draw.line(screen, (128, 128, 128), (0, i*cell_y_size), (resolution[0], i*cell_y_size))

    pygame.display.flip()
    board.update_cells()
    time.sleep(1/60)
