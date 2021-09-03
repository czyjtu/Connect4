from game.connect4 import Connect4
from ai.players import idminmax_player, query_player
from GUI.session import Session
import pickle


def main_console():
    with open("data/8ply.pkl", "rb") as f:
        data = pickle.load(f)
    game = Connect4()
    game.play_game(lambda *args: idminmax_player(*args, lookup_table=data), query_player)


def main_gui():
    session = Session()
    session.render()
    while session.running:
        session.keep_fps()
        session.handle_events()
        session.render()
        session.update()
    session.cleanup()



if __name__ == '__main__':
    main_gui()