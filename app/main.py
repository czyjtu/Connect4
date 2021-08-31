from game.connect4 import Connect4
from data.utils import process_dataset
from ai.players import minmax_player, idminmax_player, query_player
from ai.tree_search.minmax import idminmax
import pickle

def main():
    with open("data/8ply.pkl", "rb") as f:
        data = pickle.load(f)
    game = Connect4()
    game.play_game(lambda *args: idminmax_player(*args, lookup_table=data), query_player)


def main2():
    data = process_dataset()
    game = Connect4()
    s = game.initial
    for a in [3, 0, 2]:
        game.make_move(s, a)
    s.display()
    print(idminmax(game, s, data, 10))


def main3():
    game = Connect4()
    s = game.initial
    game.make_move(s, 3)
    game.make_move(s, 2)
    game.make_move(s, 3)
    game.make_move(s, 2)

    print(game.n_in_row(s, 1, 2))

    


if __name__ == '__main__':
    main()