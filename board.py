

class Board:
    def __init__(self, starting_cells: list):
        self.cells = starting_cells
        self.transformations = [[1, 0], [0, 1], [-1, 0], [0, -1], [-1, -1], [1, 1], [-1, 1], [1, -1]]
        self.unoccupied_neighbours = self._calculate_unoccupied_neighbours()
        self.new_cells = []

    def update_cells(self):

        set_of_cells = set(self.cells)

        for cell in self.cells:
            number_of_adjacent_cells = 0
            for transformation in self.transformations:
                if (cell[0] + transformation[0], cell[1] + transformation[1]) in set_of_cells:
                    number_of_adjacent_cells += 1

            if number_of_adjacent_cells == 2 or number_of_adjacent_cells == 3:
                self.new_cells.append(cell)

        for space in self.unoccupied_neighbours:
            number_of_adjacent_cells = 0
            for transformation in self.transformations:
                if (space[0] + transformation[0], space[1] + transformation[1]) in set_of_cells:
                    number_of_adjacent_cells += 1

            if space not in set(self.new_cells) and number_of_adjacent_cells == 3:
                self.new_cells.append(space)

        self.__init__(self.new_cells)

    def _calculate_unoccupied_neighbours(self):
        unoccupied_neighbours = []

        set_of_cells = set(self.cells)
        for cell in self.cells:
            for transformation in self.transformations:
                if (cell[0] + transformation[0], cell[1] + transformation[1]) not in set_of_cells:
                    unoccupied_neighbours.append((cell[0] + transformation[0], cell[1] + transformation[1]))

        return list(set(unoccupied_neighbours))
