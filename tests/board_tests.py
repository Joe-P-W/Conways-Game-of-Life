import unittest

from board import Board


class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        test_cells = [(1, 1), (2, 1), (0, 1), (1, 2), (1, 0), (2, 2)]

        self.board = Board(test_cells)

    def test_unoccupied_cells(self):
        for cell in self.board.cells:
            self.assertTrue(cell not in self.board.unoccupied_neighbours)

        self.assertTrue(len(self.board.unoccupied_neighbours) == len(set(self.board.unoccupied_neighbours)))

    def test_living_cells(self):
        for cell in self.board.unoccupied_neighbours:
            self.assertTrue(cell not in self.board.cells)

        self.assertTrue(len(self.board.cells) == len(set(self.board.cells)))


if __name__ == "__main__":
    unittest.main()
