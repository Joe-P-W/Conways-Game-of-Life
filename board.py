

class Board:
    def __init__(self, starting_cells: list):
        self.cells = starting_cells
        self.unoccupied_neighbours = self._calculate_unoccupied_neighbours()

    def _calculate_unoccupied_neighbours(self):
        unoccupied_neighbours = []
        transformations = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        set_of_cells = set(self.cells)
        for cell in self.cells:
            for transformation in transformations:
                if (cell[0] + transformation[0], cell[1] + transformation[1]) not in set_of_cells:
                    unoccupied_neighbours.append((cell[0] + transformation[0], cell[1] + transformation[1]))

        return list(set(unoccupied_neighbours))
