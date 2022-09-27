'''Модуль тестирования игры в крестики-нолики'''

import unittest
from unittest.mock import patch

from tic_tac_game import TicTacGame


class TicTacGameTest(unittest.TestCase):
    '''Класс тестирования игры в крестики-нолики'''

    X_SIGN, O_SIGN = 'x', 'o'

    def setUp(self):
        self.game = TicTacGame()
        self.game._TicTacGame__init_game()

    def tearDown(self):
        self.game = None

    def test_init_game(self):
        '''Тестирование функции init_game'''

        board = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.assertEqual(self.game.board, board)

        available_celss = set(board)
        self.assertEqual(self.game.available_cells, available_celss)

    @patch('builtins.print')
    def test_show_board(self, mock_print):
        '''Тестирование функции show_board'''

        show_board = '1 | 2 | 3\n---------\n4 | 5 | 6\n---------\n7 | 8 | 9'

        self.game._TicTacGame__show_board()
        mock_print.assert_called_with(show_board)

    def test_check_winner_default(self):
        '''Тестирование функции check_winner на default значения'''

        check_winner = self.game._TicTacGame__check_winner

        self.assertEqual(None, check_winner(self.X_SIGN))
        self.assertEqual(None, check_winner(self.O_SIGN))

    def test_check_winner_x(self):
        '''Тестирование функции check_winner на победу крестиков'''

        check_winner = self.game._TicTacGame__check_winner

        self.game._TicTacGame__board = ['x', 'x', 'x',
                                        'o', '5', '6',
                                        'o', 'o', '9']

        with self.assertRaises(StopIteration) as context:
            check_winner(self.X_SIGN)
        self.assertEqual("Победили x'ки", str(context.exception))

    def test_check_winner_o(self):
        '''Тестирование функции check_winner на победу ноликов'''

        check_winner = self.game._TicTacGame__check_winner

        self.game._TicTacGame__board = ['x', '2', 'o',
                                        'x', 'o', '6',
                                        'o', 'o', 'x']

        with self.assertRaises(StopIteration) as context:
            check_winner(self.O_SIGN)
        self.assertEqual("Победили o'ки", str(context.exception))

    def test_check_winner_draw(self):
        '''Тестирование функции check_winner на ничью'''

        check_winner = self.game._TicTacGame__check_winner

        self.game._TicTacGame__available_cells = set()

        with self.assertRaises(StopIteration) as context:
            check_winner(self.X_SIGN)
        self.assertEqual("Ничья", str(context.exception))

    @patch('builtins.input', side_effect=['1', '20', 'z'])
    def test_validate_input(self, mock_input):
        '''Тестирование функции validate_input'''

        validate_input = self.game._TicTacGame__validate_input

        self.assertEqual('1', validate_input(self.X_SIGN))
        self.assertRaises(ValueError, validate_input, self.X_SIGN)
        self.assertRaises(ValueError, validate_input, self.X_SIGN)

    @patch('builtins.input', return_value='1')
    @patch('builtins.print')
    def test_make_move(self, mock_print, mock_input):
        '''Тестирование функции make_move'''

        self.assertEqual(len(self.game.available_cells), len(self.game.board))

        self.game._TicTacGame__make_move(self.X_SIGN)

        board = ['x', '2', '3',
                 '4', '5', '6',
                 '7', '8', '9']

        self.assertEqual(self.game.board, board)
        self.assertEqual(len(self.game.available_cells),
                         len(self.game.board) - 1)

    @patch('builtins.input', side_effect=['1', '2', '5', '3', '9'])
    @patch('builtins.print')
    def test_game_winner_x(self, mock_print, mock_input):
        '''Тестирование функции start_game на победу крестиков'''

        self.game.start_game()
        mock_print.assert_called_with("Победили x'ки")

    @patch('builtins.input', side_effect=['1', '2', '3', '5', '7', '8'])
    @patch('builtins.print')
    def test_game_winner_o(self, mock_print, mock_input):
        '''Тестирование функции start_game на победу ноликов'''

        self.game.start_game()
        mock_print.assert_called_with("Победили o'ки")

    @patch('builtins.input', side_effect=['1', '2', '4', '7', '3', '5', '6', '9', '8'])
    @patch('builtins.print')
    def test_game_winner_draw(self, mock_print, mock_input):
        '''Тестирование функции start_game на ничью'''

        self.game.start_game()
        mock_print.assert_called_with("Ничья")


if __name__ == 'main':
    unittest.main()
