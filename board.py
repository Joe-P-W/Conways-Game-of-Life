

class Board:
    def __init__(self, starting_cells: list):
        self.cells = starting_cells
        self.unoccupied_neighbours = abs(self)

    def __next__(self):
        _transformations = [(1, 0), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        new_cells = []
        set_cells = set(self.cells)

        for cell in self:
            number_of_adjacent_cells = 0
            for transformation in _transformations:
                if (cell[0] + transformation[0], cell[1] + transformation[1]) in set_cells:
                    number_of_adjacent_cells += 1

            if number_of_adjacent_cells == 2 or number_of_adjacent_cells == 3:
                new_cells.append(cell)

        for space in self.unoccupied_neighbours:
            number_of_adjacent_cells = 0
            for transformation in _transformations:
                if (space[0] + transformation[0], space[1] + transformation[1]) in set_cells:
                    number_of_adjacent_cells += 1

            if space not in set_cells and number_of_adjacent_cells == 3:
                new_cells.append(space)

        self.__init__(new_cells)

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
        unoccupied_neighbours = []
        _transformations = [
            (1, 0), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, 1), (-1, 1), (1, -1)
        ]

        for cell in self:
            for transformation in _transformations:
                space = (cell[0] + transformation[0], cell[1] + transformation[1])
                if space not in self.cells:
                    unoccupied_neighbours.append(space)

        return list(set(unoccupied_neighbours))

    def absolute_position(self, _resolution, cell_x_size, cell_y_size, _squares):

        return [((cell[0] / _squares) * _resolution[0], (cell[1] / _squares) * _resolution[0], cell_x_size, cell_y_size)
                for cell in self]

    def translate(self, delta_x, delta_y):
        self.__init__([(cell[0] + delta_x, cell[1] + delta_y) for cell in self])
