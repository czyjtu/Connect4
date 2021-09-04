import pandas as pd
import numpy as np


def convert_row(board):
    pl1_fun = lambda e: 1 if e == 'x' else 0
    pl2_fun = lambda e: 1 if e == 'o' else 0
    pl1_rev = np.zeros((7,7), dtype=np.uint)
    pl2_rev = np.zeros((7,7), dtype=np.uint)
    pl1_rev[:, :-1] = np.array(list(map(pl1_fun, board)), dtype=np.uint).reshape(7, 6)
    pl2_rev[:, :-1] = np.array(list(map(pl2_fun, board)), dtype=np.uint).reshape(7, 6)

    return pl1_rev.reshape(-1), pl2_rev.reshape(-1)


def process_dataset():
    print("loading started")
    utilities = {'win': 1, 'loss': -1, 'draw': 0}
    data = {}
    df = pd.read_csv("data/connect-4.data", names=list(range(1, 44)))
    for idx, row in df.iterrows():
        player1, player2 = convert_row(np.array(row.iloc[:-1], dtype=str))
        if sum(player1 + player2) != 8:
            print("7 wrong number of moves at index: ", idx)
        utility = utilities[str(row.iloc[-1])]
        pl1_int = int("".join(np.array(player1, dtype=str))[::-1], 2)
        pl2_int = int("".join(np.array(player2, dtype=str))[::-1], 2)
        board = (pl1_int, pl2_int)
        board_mirror = mirror_board(board)
        data[board] = utility
        data[board_mirror] = utility
    print("loading finished")
    return data


def mirror_board(boards):
    pl1 = np.array(list("{:b}".format(boards[0]).zfill(49))).reshape(7,7)
    pl2 = np.array(list("{:b}".format(boards[1]).zfill(49))).reshape(7, 7)
    pl1_mirror = np.flip(pl1, 0).reshape(-1)
    pl2_mirror = np.flip(pl2, 0).reshape(-1)
    return int("".join(pl1_mirror), 2), int("".join(pl2_mirror), 2)


def process_dataset_3():
    print("loading started")
    utilities = {'win': 1, 'loss': -1, 'draw': 0.5}
    data_win = {}
    data_loss = {}
    data_draw = {}
    df = pd.read_csv("data/connect-4.data", names=list(range(1, 44)))
    for idx, row in df.iterrows():
        player1, player2 = convert_row(np.array(row.iloc[:-1], dtype=str))
        if sum(player1 + player2) != 8:
            print("7 wrong number of moves at index: ", idx)
        utility = utilities[str(row.iloc[-1])]
        pl1_int = int("".join(np.array(player1, dtype=str))[::-1], 2)
        pl2_int = int("".join(np.array(player2, dtype=str))[::-1], 2)
        board = (pl1_int, pl2_int)
        board_mirror = mirror_board(board)
        if utility == utilities['win']:
            data_win[board] = utility
            data_win[board_mirror] = utility
        elif utility == utilities['loss']:
            data_loss[board] = utility
            data_loss[board_mirror] = utility
        elif utility == utilities['draw']:
            data_draw[board] = utility
            data_draw[board_mirror] = utility
    print("loading finished")
    return data_win, data_loss, data_draw


def save_3():
    import pickle
    dw, dl, dd = process_dataset_3()
    with open("data/8ply_win.pkl", "wb") as f:
        pickle.dump(dw, f)
    with open("data/8ply_loss.pkl", "wb") as f:
        pickle.dump(dl, f)
    with open("data/8ply_draw.pkl", "wb") as f:
        pickle.dump(dd, f)

if __name__ == '__main__':
    save_3()
