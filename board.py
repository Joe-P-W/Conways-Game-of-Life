import json
import time
from typing import Union


class Board:
    def __init__(self, starting_cells: Union[list, set], _resolution: tuple, _squares: int):
        self.cells = starting_cells
        self.resolution = _resolution
        self.squares = _squares
        self.cell_x_size = _resolution[0] / _squares
        self.cell_y_size = _resolution[1] / _squares
        self._transformations = [(1, 0), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        self._unoccupied_neighbours = self._neighbours()

    def __next__(self):
        set_cells = set(self.cells)
        new_cells = [(cell_x, cell_y)
                     for cell_x, cell_y in self
                     if len([True for delta_x, delta_y in self._transformations
                             if (cell_x + delta_x, cell_y + delta_y) in set_cells]) in {2, 3}]

        new_cells += [(space_x, space_y) for space_x, space_y in self._unoccupied_neighbours
                      if len([True for delta_x, delta_y in self._transformations
                              if (space_x + delta_x, space_y + delta_y) in set_cells]) == 3]

        self.cells = set(new_cells)
        self._unoccupied_neighbours = self._neighbours()

    def __getitem__(self, item):
        return self.cells[item]

    def __len__(self):
        return len(self.cells)

    def __iadd__(self, other):
        if other not in self:
            self.cells.append(other)

        return self

    def __isub__(self, other):
        if other in self:
            self.cells.remove(other)

        return self

    def __contains__(self, item):
        return item in set(self.cells)

    def __iter__(self):
        return iter(self.cells)

    def __abs__(self):
        return [((cell_x / self.squares) * self.resolution[0], (cell_y / self.squares) * self.resolution[0],
                self.cell_x_size, self.cell_y_size) for cell_x, cell_y in self]

    def translate(self, delta_x, delta_y):
        self.cells = [(cell_x + delta_x, cell_y + delta_y) for cell_x, cell_y in self]
        self._unoccupied_neighbours = self._neighbours()

    def zoom(self, direction):
        self.squares += direction
        if self.squares < 2:
            self.squares = 2

        self.cell_x_size = self.resolution[0] / self.squares
        self.cell_y_size = self.resolution[1] / self.squares

    def _neighbours(self):
        return set([(cell_x + delta_x, cell_y + delta_y)
                    for cell_x, cell_y in self
                    for delta_x, delta_y in self._transformations
                    if (cell_x + delta_x, cell_y + delta_y) not in self.cells])


if __name__ == "__main__":
    with open("saved_starts/glider_gun.json", "r") as test_file:
        test_cells = [tuple(cell) for cell in json.load(test_file)["start_cells"]]

    board = Board(test_cells, (600, 600), 20)
    iterations = 2000
    t1 = time.time()
    for _ in range(iterations):
        next(board)

    print((time.time() - t1)/iterations)
