from game.connect4 import Connect4
from data.utils import process_dataset
from ai.players import minmax_player, idminmax_player
from ai.tree_search.minmax import idminmax


def main():
    data = process_dataset()
    lookup_table = {}
    game = Connect4()
    game.play_game(lambda *args: idminmax_player(*args, data=data, lookup_table=lookup_table), lambda *args: minmax_player(*args, data))


def main2():
    data = process_dataset()
    game = Connect4()
    s = game.initial
    for a in [3, 0, 2]:
        game.make_move(s, a)
    s.display()
    print(idminmax(game, s, data, 10))


def idminmax_main():
    data = process_dataset()
    game = Connect4()
    s = game.initial
    print(idminmax(game, s, data, 10))


if __name__ == '__main__':
    main()