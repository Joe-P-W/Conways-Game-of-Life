import sys
import time
import pygame

from board import Board

pygame.init()
resolution = (600, 600)
squares = 20
screen = pygame.display.set_mode(resolution)
cell_x_size = resolution[0] / squares
cell_y_size = resolution[1] / squares
initialising_board = True
start_cells = []

while initialising_board:
    screen.fill((255, 255, 255))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                mouse_x = round(mouse_pos[0]/squares, ndigits=0)
                mouse_y = round(mouse_pos[1]/squares, ndigits=0)

                square = (mouse_x, mouse_y)
                if square not in start_cells:
                    start_cells.append(square)
                else:
                    start_cells.remove(square)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_ENTER:
                initialising_board = False

    for cell in start_cells:
        pos = ((cell[0] / squares) * resolution[0], (cell[1] / squares) * resolution[0], cell_x_size, cell_y_size)

        pygame.draw.rect(screen, (0, 0, 0), pos)

    for i in range(int(resolution[0]/squares)):
        pygame.draw.line(screen, (128, 128, 128), (i*cell_x_size, 0), (i*cell_x_size, resolution[1]))

    for i in range(int(resolution[1]/squares)):
        pygame.draw.line(screen, (128, 128, 128), (0, i*cell_y_size), (resolution[0], i*cell_y_size))

    pygame.display.flip()


board = Board(start_cells)

while True:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    for cell in board.cells:
        pos = ((cell[0] / squares) * resolution[0], (cell[1] / squares) * resolution[0], cell_x_size, cell_y_size)

        pygame.draw.rect(screen, (0, 0, 0), pos)

    for i in range(int(resolution[0]/squares)):
        pygame.draw.line(screen, (128, 128, 128), (i*cell_x_size, 0), (i*cell_x_size, resolution[1]))

    for i in range(int(resolution[1]/squares)):
        pygame.draw.line(screen, (128, 128, 128), (0, i*cell_y_size), (resolution[0], i*cell_y_size))

    pygame.display.flip()

    board.update_cells()
    time.sleep(0.5)



