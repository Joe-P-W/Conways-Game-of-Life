import json
import time
from typing import Set, Tuple, Union


class Board:
    def __init__(self, starting_cells: Set[Tuple[Union[int, float], Union[int, float]]],
                 _resolution: Tuple[int, int], _squares: int):
        self.cells = starting_cells
        self.resolution = _resolution
        self.squares = _squares
        self.cell_x_size = _resolution[0] / _squares
        self.cell_y_size = _resolution[1] / _squares
        self._transformations = [(1, 0), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        self._unoccupied_neighbours = +self

    def __next__(self):
        set_cells = self.cells
        transformations = self._transformations
        new_cells = {(cell_x, cell_y)
                     for cell_x, cell_y in self
                     if len([(cell_x + delta_x, cell_y + delta_y) for delta_x, delta_y in transformations
                             if (cell_x + delta_x, cell_y + delta_y) in set_cells]) in {2, 3}}

        new_cells.update({(space_x, space_y) for space_x, space_y in self._unoccupied_neighbours
                         if len([True for delta_x, delta_y in transformations
                                 if (space_x + delta_x, space_y + delta_y) in set_cells]) == 3})

        self.cells = new_cells
        self._unoccupied_neighbours = +self

    def __getitem__(self, item):
        return list(self.cells)[item]

    def __len__(self):
        return len(self.cells)

    def __iadd__(self, other):
        self.cells.add(other)

        return self

    def __isub__(self, other):
        self.cells.discard(other)

        return self

    def __contains__(self, item):
        return item in self.cells

    def __iter__(self):
        return iter(self.cells)

    def __abs__(self):
        return [((cell_x / self.squares) * self.resolution[0], (cell_y / self.squares) * self.resolution[0],
                self.cell_x_size, self.cell_y_size) for cell_x, cell_y in self]

    def __pos__(self):
        return {(cell_x + delta_x, cell_y + delta_y)
                for cell_x, cell_y in self.cells
                for delta_x, delta_y in self._transformations
                if (cell_x + delta_x, cell_y + delta_y) not in self.cells}

    def translate(self, delta_x, delta_y):
        self.cells = [(cell_x + delta_x, cell_y + delta_y) for cell_x, cell_y in self]
        self._unoccupied_neighbours = +self

    def zoom(self, direction):
        self.squares += direction
        if self.squares < 2:
            self.squares = 2

        self.cell_x_size = self.resolution[0] / self.squares
        self.cell_y_size = self.resolution[1] / self.squares


if __name__ == "__main__":
    with open("saved_starts/glider_gun.json", "r") as test_file:
        test_cells = {tuple(cell) for cell in json.load(test_file)["start_cells"]}

    board = Board(test_cells, (600, 600), 20)
    iterations = 2000
    t1 = time.time()
    for _ in range(iterations):
        next(board)

    print((time.time() - t1)/iterations)
