'''Модуль реализации игры в крестики-нолики'''


class TicTacGame:
    '''Класс игры в крестики-нолики'''

    SIZE = 3

    WIN_TACTICS = (
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 4, 8), (2, 4, 6))

    X_SIGN, O_SIGN = 'x', 'o'

    def __init__(self):
        self.board = None
        self.available_cells = None

    def init_game(self):
        '''Функция инициализации игровой доски'''

        self.board = [str(i) for i in range(1, self.SIZE ** 2 + 1)]
        self.available_cells = set(self.board)

    def start_game(self):
        '''Функция для старта игры'''

        while True:
            try:
                self.make_move(self.X_SIGN)
                self.make_move(self.O_SIGN)
            except ValueError as error:
                print(error)
            except StopIteration as stop:
                print(stop.value)
                break

    def make_move(self, sign):
        '''Функция выполнения хода в игре'''

        self.show_board()

        num = self.validate_input(sign)

        self.board[num] = sign
        self.available_cells.discard(str(num + 1))

        self.check_winner(sign)

    def show_board(self):
        '''Функция печати игровой доски'''

        for i in range(0, self.SIZE ** 2, self.SIZE):
            row = self.board[i:i + self.SIZE]
            print(' | '.join(row), '----------', sep='\n')

    def validate_input(self, sign):
        '''Функция валидации пользовательского ввода'''

        answer = input(f'Куда поставить {sign}? ')

        if not answer.isdigit():
            raise ValueError('Значение должно быть цифрой')

        if answer not in self.available_cells:
            raise ValueError('Цифра должна быть свободна на доске')

        return int(answer) - 1

    def check_winner(self, sign):
        '''Функция определения победителя'''

        if len(self.available_cells) == 0:
            raise StopIteration('Ничья')

        for tactic in self.WIN_TACTICS:
            is_row_win = map(lambda i: self.board[i] == sign, tactic)
            if all(is_row_win):
                raise StopIteration(f"Победили {sign}'ки")


if __name__ == '__main__':
    game = TicTacGame()
    game.init_game()
    game.start_game()
