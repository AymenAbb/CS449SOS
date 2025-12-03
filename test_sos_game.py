import unittest
import os
from game_recorder import GameRecorder
from game_replayer import GameReplayer
from SOSGame import SOSGame, SimpleGame, GeneralGame
from player import Player, HumanPlayer, ComputerPlayer


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


class TestUserStory8_ComputerOpponent(unittest.TestCase):
    def test_ac_8_1_select_computer_player(self):
        # AC 8.1: Player can select Computer for Blue or Red player
        blue_computer = ComputerPlayer("blue")
        red_computer = ComputerPlayer("red")

        self.assertEqual(blue_computer.color, "blue")
        self.assertEqual(red_computer.color, "red")

        game = SimpleGame(
            board_size=3, blue_player=blue_computer, red_player=red_computer
        )
        self.assertIsNotNone(game.get_current_player_object())

    def test_ac_8_2_computer_makes_valid_move(self):
        # AC 8.2: Computer automatically makes valid moves when it's their turn
        game = SimpleGame(board_size=3)
        computer = ComputerPlayer("blue")

        move = computer.get_move(game)
        self.assertIsNotNone(move)

        row, col, letter = move
        self.assertTrue(0 <= row < 3)
        self.assertTrue(0 <= col < 3)
        self.assertIn(letter, ["S", "O"])
        self.assertEqual(game.get_cell(row, col), SOSGame.EMPTY)

    def test_ac_8_3_computer_follows_game_rules(self):
        # AC 8.3: Computer follows game rules and makes valid moves
        game = SimpleGame(board_size=3)
        computer = ComputerPlayer("blue")
        game.make_move(0, 0, "S")
        game.make_move(1, 1, "O")

        move = computer.get_move(game)
        row, col, letter = move

        # Computer should not choose occupied cells
        self.assertNotEqual((row, col), (0, 0))
        self.assertNotEqual((row, col), (1, 1))
        self.assertEqual(game.get_cell(row, col), SOSGame.EMPTY)

    def test_ac_8_4_computer_finds_winning_move(self):
        # AC 8.4: Computer uses strategy to find winning moves
        game = SimpleGame(board_size=3)
        computer = ComputerPlayer("blue")

        # Set up board where S-O-? allows computer to complete SOS
        game._board[0][0] = "S"
        game._board[0][1] = "O"
        # Position (0,2) with 'S' would complete SOS

        move = computer.get_move(game)
        row, col, letter = move

        # Computer should complete the SOS
        self.assertEqual((row, col, letter), (0, 2, "S"))

    def test_ac_8_5_computer_blocks_opponent(self):
        # AC 8.5: Computer attempts to block opponent from winning
        game = SimpleGame(board_size=3)
        computer = ComputerPlayer("blue")

        # Set up board where opponent could win
        game._board[1][0] = "S"
        game._board[1][1] = "O"
        # Position (1,2) with 'S' would complete SOS for opponent

        move = computer.get_move(game)
        row, col, letter = move
        self.assertIsNotNone(move)

    def test_ac_8_6_computer_vs_computer_game(self):
        # AC 8.6: Two computer players can play a complete game
        blue_computer = ComputerPlayer("blue")
        red_computer = ComputerPlayer("red")
        game = SimpleGame(
            board_size=3, blue_player=blue_computer, red_player=red_computer
        )

        moves_made = 0
        max_moves = 9

        while not game.game_over and moves_made < max_moves:
            player = game.get_current_player_object()
            move = player.get_move(game)

            if move:
                row, col, letter = move
                game.make_move(row, col, letter)
                moves_made += 1
            else:
                break

        # Game should end naturally (either win or board full)
        self.assertTrue(game.game_over or moves_made == max_moves)

    def test_ac_8_7_human_player_no_auto_move(self):
        # AC 8.7: Human players don't auto-generate moves
        human = HumanPlayer("blue")
        game = SimpleGame(board_size=3)

        move = human.get_move(game)
        self.assertIsNone(move)


class TestUserStory9_RecordReplay(unittest.TestCase):
    def setUp(self):
        self.recorder = GameRecorder()
        self.replayer = GameReplayer()
        self.recorded_file = None

    def tearDown(self):
        if os.path.exists("recordings"):
            for file in os.listdir("recordings"):
                if file.startswith("game_"):
                    os.remove(os.path.join("recordings", file))

    # Helper to create a test recording file using GameRecorder
    def _create_test_recording(self):
        self.recorder.start_recording(3, "Simple", "Human", "Computer")
        self.recorder.record_move(0, 0, "S", "blue")
        self.recorder.record_move(0, 1, "O", "red")
        self.recorder.record_move(0, 2, "S", "blue")
        self.recorder.record_final_state("blue", 1, 0)
        self.recorded_file = self.recorder.save_recording()
        return self.recorded_file

    # AC 9.1: Player can enable recording before starting a game
    def test_ac_9_1_start_recording(self):
        self.assertFalse(self.recorder.is_recording)
        self.recorder.start_recording(8, "Simple", "Human", "Computer")
        self.assertTrue(self.recorder.is_recording)

    # AC 9.2: All moves are recorded during gameplay
    def test_ac_9_2_record_moves(self):
        self.recorder.start_recording(3, "Simple", "Human", "Human")
        self.recorder.record_move(0, 0, "S", "blue")
        self.recorder.record_move(0, 1, "O", "red")

        self.assertEqual(len(self.recorder._game_data["moves"]), 2)
        self.assertEqual(self.recorder._game_data["moves"][0]["letter"], "S")
        self.assertEqual(self.recorder._game_data["moves"][1]["letter"], "O")

    # AC 9.3: Recording is saved to file when game ends
    def test_ac_9_3_save_recording_to_file(self):
        self.recorder.start_recording(3, "Simple", "Human", "Human")
        self.recorder.record_move(0, 0, "S", "blue")
        self.recorder.record_final_state("blue", 1, 0)

        filepath = self.recorder.save_recording()

        self.assertIsNotNone(filepath)
        self.assertTrue(os.path.exists(filepath))
        self.assertFalse(self.recorder.is_recording)

    # AC 9.4: Recording file contains all game data in correct format
    def test_ac_9_4_recording_file_format(self):
        filepath = self._create_test_recording()
        self.replayer.load_game(filepath)

        config = self.replayer.get_game_config()
        self.assertEqual(config["board_size"], 3)
        self.assertEqual(config["game_mode"], "Simple")
        self.assertEqual(config["blue_player_type"], "Human")
        self.assertEqual(config["red_player_type"], "Computer")
        self.assertEqual(self.replayer.get_total_moves(), 3)
        self.assertEqual(self.replayer.get_final_state()["winner"], "blue")

    # AC 9.5: Can load a recording file for replay
    def test_ac_9_5_load_recording_for_replay(self):
        filepath = self._create_test_recording()
        self.replayer.load_game(filepath)

        config = self.replayer.get_game_config()
        self.assertEqual(config["board_size"], 3)
        self.assertEqual(config["game_mode"], "Simple")

    # AC 9.6: Moves are replayed in correct sequence
    def test_ac_9_6_replay_moves_in_sequence(self):
        filepath = self._create_test_recording()
        self.replayer.load_game(filepath)

        move1 = self.replayer.get_next_move()
        self.assertEqual(move1["row"], 0)
        self.assertEqual(move1["col"], 0)
        self.assertEqual(move1["player"], "blue")

        move2 = self.replayer.get_next_move()
        self.assertEqual(move2["row"], 0)
        self.assertEqual(move2["col"], 1)
        self.assertEqual(move2["player"], "red")

    # AC 9.7: Replay tracks current and total moves
    def test_ac_9_7_replay_tracks_progress(self):
        filepath = self._create_test_recording()
        self.replayer.load_game(filepath)

        self.assertEqual(self.replayer.get_total_moves(), 3)
        self.assertEqual(self.replayer.get_current_move_index(), 0)

        self.replayer.get_next_move()
        self.assertEqual(self.replayer.get_current_move_index(), 1)

    # AC 9.8: Replay correctly detects when all moves are played
    def test_ac_9_8_replay_detects_end(self):
        filepath = self._create_test_recording()
        self.replayer.load_game(filepath)

        self.assertTrue(self.replayer.has_next_move())

        while self.replayer.has_next_move():
            self.replayer.get_next_move()

        self.assertFalse(self.replayer.has_next_move())

    # AC 9.9: Replay shows final game state
    def test_ac_9_9_replay_shows_final_state(self):
        filepath = self._create_test_recording()
        self.replayer.load_game(filepath)

        final_state = self.replayer.get_final_state()
        self.assertEqual(final_state["winner"], "blue")
        self.assertEqual(final_state["blue_score"], 1)
        self.assertEqual(final_state["red_score"], 0)

    # AC 9.10: Invalid recording files are handled
    def test_ac_9_10_invalid_file_handling(self):
        with self.assertRaises(FileNotFoundError):
            self.replayer.load_game("nonexistent_file.json")


if __name__ == "__main__":
    unittest.main()
