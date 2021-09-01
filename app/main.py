from game.connect4 import Connect4
from ai.players import idminmax_player, query_player
import pickle


def main():
    with open("data/8ply.pkl", "rb") as f:
        data = pickle.load(f)
    game = Connect4()
    game.play_game(lambda *args: idminmax_player(*args, lookup_table=data), query_player)


if __name__ == '__main__':
    main()