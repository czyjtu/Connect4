from game.connect4 import Connect4
from ai.players import minmax_player
from ai.tree_search.mcts import MCTS
from GUI.session import Session
import pickle


def main_console():
    with open("data/8ply.pkl", "rb") as f:
        data = pickle.load(f)
    game = Connect4()
    game.play_game(minmax_player, minmax_player)#lambda *args: minmax_player(*args, lookup_table=data))


def main_gui():
    session = Session()
    session.render()
    while session.running:
        session.keep_fps()
        session.handle_events()
        session.render()
        session.update()
    session.cleanup()


def pickle_mcts():
    game = Connect4()
    mcts = MCTS(game=game, state=game.initial)
    mcts.train(200000)
    with open("data/mcts_root_200k_1_4.pkl", "wb") as f:
        pickle.dump(mcts.root, f)




if __name__ == '__main__':
    main_gui()
    # pickle_mcts()