import numpy as np
from random import choice
from typing import List


class Player:
    players: List[object] = []

    def __init__(self, name, xo):
        self.name = name
        self.xo = xo
        self.combinations = []
        self.__class__.players.append(self)

    def __str__(self):
        return f'Player {self.name}'

    # debugging purposes
    def __repr__(self):
        return f'{self.name}'


class Board:

    def __init__(self):
        self.fields = [["" for _ in range(3)] for _ in range(3)]

    def show(self):
        print("=====")
        for row in self.fields:
            print(row)
        print("=====")

    def move(self, player: Player, x, y):
        try:
            self.fields[x][y] = player.xo
            player.combinations.append([x, y])
        except IndexError:
            print("Not valid position, try again")


def get_winner(p1: Player, p2: Player) -> Player:
    winning_combs = [
        # vertical
        [[0, 0], [1, 0], [2, 0]],
        [[0, 1], [1, 1], [2, 1]],
        [[0, 2], [1, 2], [2, 2]],
        # horizontal
        [[0, 0], [0, 1], [0, 2]],
        [[1, 0], [1, 1], [1, 2]],
        [[2, 0], [2, 1], [2, 2]],
        # diagonal
        [[0, 0], [1, 1], [2, 2]],
        [[2, 0], [1, 1], [0, 0]],
    ]

    won_player: Player = None

    for win_comb in winning_combs:
        p1_win_chance = 0
        p2_win_chance = 0

        for p1_comb in p1.combinations:
            if p1_comb in win_comb:
                p1_win_chance += 1

        for p2_comb in p2.combinations:
            if p2_comb in win_comb:
                p2_win_chance += 1

        if p1_win_chance == 3:
            won_player = p1

        elif p2_win_chance == 3:
            won_player = p2

    return won_player


def input_cords(board: Board) -> tuple:
    while True:
        try:
            x, y = [int(x) for x in input(
                "Specify X and Y position of your choice (with space for instance: 0 0 >>").split()]
        except (ValueError, TypeError):
            print("Try again, wrong values")
            continue

        if board.fields[x][y] == '':
            return (x, y)
        else:
            print('Invalid field! Please try again')


def draw_player():
    return choice(Player.players)


def get_opponent(first_player: Player):
    return Player.players[1] if Player.players.index(first_player) == 0 else Player.players[0]


def create_players():
    p1_name = input("Player 1, What's your name? >>")
    p2_name = input("Player 2, What's your name? >>")

    while True:
        p1_sign = input("Player 1, Would you like to be X or O? >>").upper()

        if p1_sign == "X" or p1_sign == "O":  # prevent from using non X or O field
            p2_sign = "X" if p1_sign == "O" else "O"
            break
        else:
            print("You can be only X or O, please try again")

    Player(p1_name, p1_sign)
    Player(p2_name, p2_sign)


def check_winner(winner: Player, board: Board):
    empty_fields = np.any(np.ravel(board.fields) == '')

    if not empty_fields and winner == None:
        return "Tie!"
    else:
        return f"Winner -> {winner}!"


def main():
    create_players()

    board = Board()
    board.show()

    first_player: Player = draw_player()
    second_player: Player = get_opponent(first_player)

    print(f'{first_player} starts!')

    # main logic of the game
    while True:
        winner = get_winner(first_player, second_player)

        if winner == None:
            x1, y1 = input_cords(board)
            board.move(first_player, x1, y1)
            board.show()

            x2, y2 = input_cords(board)
            board.move(second_player, x2, y2)
            board.show()

            winner = get_winner(first_player, second_player)

        else:
            print(check_winner(winner, board))
            break


if __name__ == '__main__':
    main()
