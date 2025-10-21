# Unit tests, one test per acceptance criterion.

import unittest
from SOSGame import SOSGame


class TestUserStory1_ChooseBoardSize(unittest.TestCase):
    def test_ac_1_1_size_options_valid(self):
        # AC 1.1: Size validation for n>=3, reject n<3.

        game = SOSGame(board_size=3)
        self.assertEqual(game.board_size, 3)

        game2 = SOSGame(board_size=10)
        self.assertEqual(game2.board_size, 10)

        with self.assertRaises(ValueError):
            SOSGame(board_size=2)

    def test_ac_1_2_board_renders(self):
        game = SOSGame(board_size=5)

        # Check dimensions for all empty cells
        for row in range(5):
            for col in range(5):
                self.assertEqual(game.get_cell(row, col), SOSGame.EMPTY)


if __name__ == "__main__":
    unittest.main(verbosity=1)
