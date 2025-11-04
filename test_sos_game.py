import unittest
from SOSGame import SOSGame, SimpleGame, GeneralGame


class TestUserStory1_ChooseBoardSize(unittest.TestCase):
    def test_ac_1_1_size_options_valid(self):
        game = SimpleGame(board_size=3)
        self.assertEqual(game.board_size, 3)

        game = SimpleGame(board_size=10)
        self.assertEqual(game.board_size, 10)

        with self.assertRaises(ValueError):
            SimpleGame(board_size=2)

    def test_ac_1_2_board_renders(self):
        game = SimpleGame(board_size=5)
        self.assertEqual(game.board_size, 5)

        for row in range(5):
            for col in range(5):
                self.assertEqual(game.get_cell(row, col), SOSGame.EMPTY)


class TestUserStory2_ChooseGameMode(unittest.TestCase):
    def test_ac_2_1_menu_select(self):
        simple_game = SimpleGame()
        self.assertEqual(simple_game.game_mode, SOSGame.SIMPLE)

        general_game = GeneralGame()
        self.assertEqual(general_game.game_mode, SOSGame.GENERAL)

    def test_ac_2_2_post_menu_selection(self):
        game = GeneralGame(board_size=4)
        self.assertEqual(game.game_mode, SOSGame.GENERAL)
        self.assertEqual(game.current_player, SOSGame.BLUE)


class TestUserStory3_StartNewGame(unittest.TestCase):
    def test_ac_3_1_reset_state(self):
        game = SimpleGame()
        game.make_move(0, 0, "S")
        game.reset_game()

        self.assertEqual(game.get_cell(0, 0), SOSGame.EMPTY)
        self.assertEqual(game.current_player, SOSGame.BLUE)

    def test_ac_3_2_reconfigure_size_and_mode(self):
        game = SimpleGame(board_size=5)
        game.reset_game(board_size=8)
        self.assertEqual(game.board_size, 8)

        game = GeneralGame(board_size=6)
        self.assertEqual(game.game_mode, SOSGame.GENERAL)


class TestUserStory4_MakeMoveSimpleGame(unittest.TestCase):
    def test_ac_4_1_valid_placement(self):
        game = SimpleGame()
        self.assertTrue(game.make_move(0, 0, "S"))
        self.assertEqual(game.get_cell(0, 0), "S")
        self.assertEqual(game.current_player, SOSGame.RED)

        self.assertTrue(game.make_move(1, 1, "O"))
        self.assertEqual(game.current_player, SOSGame.BLUE)

    # AC 4.2 is tested in UI

    def test_ac_4_3_invalid_move_handling(self):
        game = SimpleGame()
        game.make_move(0, 0, "S")

        self.assertFalse(game.make_move(0, 0, "O"))
        self.assertFalse(game.make_move(10, 10, "S"))


class TestUserStory5_SimpleGameOver(unittest.TestCase):
    def test_ac_5_1_first_sos_wins(self):
        game = SimpleGame(board_size=3)
        game.make_move(0, 0, "S")
        game.make_move(1, 0, "S")
        game.make_move(0, 1, "O")
        game.make_move(1, 1, "O")
        game.make_move(0, 2, "S")

        self.assertTrue(game.game_over)
        self.assertEqual(game.winner, SOSGame.BLUE)
        self.assertEqual(game.blue_score, 1)

    def test_ac_5_2_board_full_draw(self):
        game = SimpleGame(board_size=3)
        moves = [
            (0, 0, "O"),
            (0, 1, "O"),
            (0, 2, "O"),
            (1, 0, "O"),
            (1, 1, "S"),
            (1, 2, "O"),
            (2, 0, "O"),
            (2, 1, "O"),
            (2, 2, "S"),
        ]
        for row, col, letter in moves:
            game.make_move(row, col, letter)

        self.assertTrue(game.game_over)
        self.assertIsNone(game.winner)


class TestUserStory6_MakeMoveGeneralGame(unittest.TestCase):

    # AC 6.1 is tested in UI

    def test_ac_6_2_invalid_move_handling(self):
        game = GeneralGame()
        game.make_move(2, 2, "S")

        self.assertFalse(game.make_move(2, 2, "O"))
        self.assertFalse(game.make_move(10, 10, "S"))

    def test_ac_6_3_no_sos_alternates_turn(self):
        game = GeneralGame()
        game.make_move(0, 0, "S")
        self.assertEqual(game.current_player, SOSGame.RED)

        game.make_move(0, 1, "O")
        self.assertEqual(game.current_player, SOSGame.BLUE)


class TestUserStory7_GeneralGameOver(unittest.TestCase):
    def test_ac_7_1_continues_until_full(self):
        game = GeneralGame(board_size=3)
        game.make_move(0, 0, "S")
        game.make_move(0, 1, "O")
        game.make_move(0, 2, "S")

        self.assertFalse(game.game_over)

    def test_ac_7_2_most_sos_wins(self):
        game = GeneralGame(board_size=3)
        game.make_move(0, 0, "S")
        game.make_move(1, 0, "S")
        game.make_move(0, 1, "O")
        game.make_move(1, 1, "O")
        game.make_move(0, 2, "S")

        game.make_move(2, 0, "O")
        game.make_move(2, 1, "O")
        game.make_move(1, 2, "O")
        game.make_move(2, 2, "O")

        self.assertTrue(game.game_over)
        self.assertEqual(game.winner, SOSGame.BLUE)
        self.assertGreater(game.blue_score, game.red_score)

    def test_ac_7_3_sos_player_continues(self):
        game = GeneralGame(board_size=3)
        game.make_move(0, 0, "S")
        game.make_move(1, 0, "S")
        game.make_move(0, 1, "O")
        game.make_move(1, 1, "O")

        current = game.current_player
        game.make_move(0, 2, "S")

        self.assertEqual(game.current_player, current)
        self.assertEqual(game.blue_score, 1)


if __name__ == "__main__":
    unittest.main()
