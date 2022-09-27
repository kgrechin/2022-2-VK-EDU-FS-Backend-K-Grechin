'''Модуль реализации игры в крестики-нолики'''


class TicTacGame:
    '''Класс игры в крестики-нолики'''

    __SIZE = 3

    __WIN_TACTICS = (
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 4, 8), (2, 4, 6))

    __X_SIGN, __O_SIGN = 'x', 'o'

    def __init__(self):
        self.__board = self.__available_cells = None

    @property
    def board(self):
        '''Функция для получения игровой доски'''
        return self.__board.copy()

    @property
    def available_cells(self):
        '''Функция для получения доступных клеток'''
        return self.__available_cells.copy()

    def start_game(self):
        '''Функция для старта игры'''
        self.__init_game()

        while True:
            try:
                self.__make_move(self.__X_SIGN)
                self.__make_move(self.__O_SIGN)
            except ValueError as error:
                print(error)
            except StopIteration as stop:
                print(stop.value)
                break

    def __init_game(self):
        self.__board = [str(i) for i in range(1, self.__SIZE ** 2 + 1)]
        self.__available_cells = set(self.__board)

    def __show_board(self):
        print('\n---------\n'.join(' | '.join(self.__board[i:i + self.__SIZE])
                                   for i in range(0, self.__SIZE ** 2, self.__SIZE)))

    def __make_move(self, sign):
        self.__show_board()
        num = self.__validate_input(sign)

        self.__board[int(num) - 1] = sign
        self.__available_cells.discard(num)

        self.__check_winner(sign)

    def __validate_input(self, sign):
        num = input(f'Куда поставить {sign}? ')
        if num not in self.__available_cells:
            raise ValueError('Номер клетки - свободная цифра на доске')
        return num

    def __check_winner(self, sign):
        if len(self.__available_cells) == 0:
            raise StopIteration('Ничья')
        if any(map(lambda tactic: all(map(lambda x: self.__board[x] == sign, tactic)),
                   self.__WIN_TACTICS)):
            raise StopIteration(f"Победили {sign}'ки")


if __name__ == '__main__':
    game = TicTacGame()
    game.start_game()
