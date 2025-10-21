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


class TestUserStory2_ChooseGameMode(unittest.TestCase):

    def test_ac_2_1_menu_select(self):
        game_simple = SOSGame(game_mode=SOSGame.SIMPLE)
        self.assertEqual(game_simple.game_mode, SOSGame.SIMPLE)

        game_general = SOSGame(game_mode=SOSGame.GENERAL)
        self.assertEqual(game_general.game_mode, SOSGame.GENERAL)

    def test_ac_2_2_post_menu_selection(self):
        # Rule application
        game = SOSGame(board_size=4, game_mode=SOSGame.GENERAL)

        self.assertEqual(game.game_mode, SOSGame.GENERAL)
        self.assertEqual(game.current_player, SOSGame.BLUE)


class TestUserStory3_StartNewGame(unittest.TestCase):
    def test_ac_3_1_reset_state(self):
        # Reset grid, scores, and becomes blue's turn
        game = SOSGame(board_size=3)
        game.make_move(0, 0, "S")
        game.make_move(1, 1, "O")

        game.reset_game()

        # Grid cleared
        for row in range(3):
            for col in range(3):
                self.assertEqual(game.get_cell(row, col), SOSGame.EMPTY)

        self.assertEqual(game.current_player, SOSGame.BLUE)

    def test_ac_3_2_reconfigure_size_and_mode(self):
        game = SOSGame(board_size=5, game_mode=SOSGame.SIMPLE)

        game.reset_game(board_size=8, game_mode=SOSGame.GENERAL)

        self.assertEqual(game.board_size, 8)
        self.assertEqual(game.game_mode, SOSGame.GENERAL)


if __name__ == "__main__":
    unittest.main(verbosity=1)
