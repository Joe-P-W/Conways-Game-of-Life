

class Board:
    def __init__(self, starting_cells: list):
        self.cells = starting_cells
        self.unoccupied_neighbours = self[1]
        self.new_cells = []

    def __next__(self):
        set_of_cells = set(self.cells)
        _transformations = {(1, 0), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, 1), (-1, 1), (1, -1)}

        for cell in self.cells:
            number_of_adjacent_cells = 0
            for transformation in _transformations:
                if (cell[0] + transformation[0], cell[1] + transformation[1]) in set_of_cells:
                    number_of_adjacent_cells += 1

            if number_of_adjacent_cells == 2 or number_of_adjacent_cells == 3:
                self.new_cells.append(cell)

        for space in self.unoccupied_neighbours:
            number_of_adjacent_cells = 0
            for transformation in _transformations:
                if (space[0] + transformation[0], space[1] + transformation[1]) in set_of_cells:
                    number_of_adjacent_cells += 1

            if space not in set(self.new_cells) and number_of_adjacent_cells == 3:
                self.new_cells.append(space)

        self.__init__(self.new_cells)

    def __getitem__(self, item):
        unoccupied_neighbours = []
        _transformations = {
            (item, 0), (0, item), (-item, 0), (0, -item), (-item, -item), (item, item), (-item, item), (item, -item)
        }
        set_of_cells = set(self.cells)
        for cell in self.cells:
            for transformation in _transformations:
                if (cell[0] + transformation[0], cell[1] + transformation[1]) not in set_of_cells:
                    unoccupied_neighbours.append((cell[0] + transformation[0], cell[1] + transformation[1]))

        return list(set(unoccupied_neighbours))

    def __add__(self, other):
        self.cells = [(cell[0] + other[0], cell[1] + other[1]) for cell in self.cells]
        self.unoccupied_neighbours = [(cell[0] + other[0], cell[1] + other[1]) for cell in self.unoccupied_neighbours]

    def __len__(self):
        return len(self.cells)

    def __iadd__(self, other):
        if other not in set(self.cells):
            self.cells.append(other)

        return self

    def __isub__(self, other):
        if other in self.cells:
            self.cells.remove(other)

        return self

    def absolute_position(self, _resolution, cell_x_size, cell_y_size, _squares):

        return [((cell[0] / _squares) * _resolution[0], (cell[1] / _squares) * _resolution[0], cell_x_size, cell_y_size)
                for cell in self.cells]
