from game.connect4 import Connect4
from data.utils import process_dataset
import pandas as pd
import numpy as np
from ai.players import random_player, minmax_player, minmax_player_data


def main_minmax_data():
    data = process_dataset()
    game = Connect4()
    s = game.initial
    game.make_move(s,  0)
    print(minmax_player_data(game, s, data))


def main():
    data = process_dataset()
    game = Connect4()
    s = game.initial
    # game.make_move(s, 0)
    # game.make_move(s, 0)
    # game.make_move(s, 0)
    # game.make_move(s, 0)
    # game.make_move(s, 1)
    # game.make_move(s, 0)
    # game.make_move(s, 2)
    # game.make_move(s, 0)
    game.play_game(random_player, lambda *args: minmax_player_data(*args, data))
    # print(minmax_player_data(game, s, data))
    # print(game.get_forced(s))
    s.display()


def main2():
    game = Connect4()
    s = game.initial
    for a in [0, 0, 0, 1, 0, 1, 2, 1]:
        game.make_move(s, a)
    game.make_move(s, 1, 1)
    s.display()
    print(game.get_forced(s))

if __name__ == '__main__':
    # main_minmax_data()
    # main2()
    main()