from board import Board

board = Board([(1, 1), (2, 1)])

for cell in board.cells:
    assert cell not in board.unoccupied_neighbours
