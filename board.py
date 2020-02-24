

class Board:
    def __init__(self, starting_cells: list, _resolution: tuple, _squares: int):
        self.cells = starting_cells
        self.resolution = _resolution
        self.squares = _squares
        self.cell_x_size = _resolution[0] / _squares
        self.cell_y_size = _resolution[1] / _squares
        self._transformations = [(1, 0), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        self._unoccupied_neighbours = self.neighbours()

    def __next__(self):
        new_cells = []
        set_cells = set(self.cells)

        for cell_x, cell_y in self:
            number_of_adjacent_cells = 0
            for delta_x, delta_y in self._transformations:
                if (cell_x + delta_x, cell_y + delta_y) in set_cells:
                    number_of_adjacent_cells += 1

            if number_of_adjacent_cells == 2 or number_of_adjacent_cells == 3:
                new_cells.append((cell_x, cell_y))

        for space_x, space_y in self._unoccupied_neighbours:
            number_of_adjacent_cells = 0
            for delta_x, delta_y in self._transformations:
                if (space_x + delta_x, space_y + delta_y) in set_cells:
                    number_of_adjacent_cells += 1

            if (space_x, space_y) not in set_cells and number_of_adjacent_cells == 3:
                new_cells.append((space_x, space_y))

        self.__init__(new_cells, self.resolution, self.squares)

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
        if item in set(self.cells):
            return True
        else:
            return False

    def __iter__(self):
        return iter(self.cells)

    def __abs__(self):

        return [((cell[0] / self.squares) * self.resolution[0], (cell[1] / self.squares) * self.resolution[0],
                 self.cell_x_size, self.cell_y_size) for cell in self]

    def neighbours(self):
        unoccupied_neighbours = []

        for cell in self:
            for transformation in self._transformations:
                space = (cell[0] + transformation[0], cell[1] + transformation[1])
                if space not in self.cells:
                    unoccupied_neighbours.append(space)

        return set(unoccupied_neighbours)

    def translate(self, delta_x, delta_y):
        self.__init__([(cell_x + delta_x, cell_y + delta_y) for cell_x, cell_y in self], self.resolution, self.squares)

    def zoom(self, direction):
        self.squares += direction
        if self.squares < 2:
            self.squares = 2

        self.__init__(self.cells, self.resolution, self.squares + direction)
