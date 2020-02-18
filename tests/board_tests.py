import random
import unittest

from board import Board


class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        test_cells = [(2, 2), (1, 2), (2, 1), (3, 2), (2, 3)]

        self.board = Board(test_cells)

    def test_unoccupied_cells(self):
        for cell in self.board.cells:
            self._assert_true(cell not in self.board.unoccupied_neighbours,
                              f"{cell} in both living and unoccupied cell lists")

        self._assert_true(len(self.board.unoccupied_neighbours) == len(set(self.board.unoccupied_neighbours)),
                          "Living cells list not unique")

    def test_living_cells(self):
        for cell in self.board.unoccupied_neighbours:
            self._assert_true(cell not in self.board.cells,
                              f"{cell} in both living and unoccupied cell lists")

        self._assert_true(len(self.board.cells) == len(set(self.board.cells)), "Living cells list not unique")

    def test_one_board_update(self):
        assertion_board = [(1, 2), (2, 1), (3, 2), (2, 3), (1, 3), (3, 3), (3, 1), (1, 1)]
        self.board.update_cells()

        self._validate_board_updates(assertion_board)

    def test_two_board_updates(self):
        assertion_board = [(1, 3), (3, 3), (3, 1), (1, 1), (2, 0), (2, 4), (4, 2), (0, 2)]

        for _ in range(2):
            self.board.update_cells()

        self._validate_board_updates(assertion_board)

    def test_arbitrarily_large_number_of_board_updates(self):
        for _ in range(random.randint(20, 50)):
            self.board.update_cells()

        self._validate_board_updates(None)

    def _validate_board_updates(self, assertion_board):

        if assertion_board is not None:
            for cell in self.board.cells:
                self._assert_true(cell in assertion_board,
                                  f"{cell} from the board not in the assertion data: {assertion_board}")

            for cell in assertion_board:
                self._assert_true(cell in self.board.cells,
                                  f"{cell} from the assertion data not in the board: {self.board.cells}")

        self.test_living_cells()
        self.test_unoccupied_cells()

    def _assert_true(self, expression, failure_message):
        try:
            self.assertTrue(expression)
        except AssertionError:
            raise AssertionError(failure_message)


if __name__ == "__main__":
    unittest.main()
