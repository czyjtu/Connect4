import numpy as np


def n_in_row(state, player, n):
    directions = [1, 7, 6, 8]
    for d in directions:
        if n == 2 and state.boards[player] & (state.boards[player] >> d) != 0:
            return True
        if n == 3 and state.boards[player] & (state.boards[player] >> d) & (state.boards[player] >> 2*d)!= 0:
            return True
    return False


def eval_fun_0(game, state, player):
    if state.utility == 1:
        return 1
    scores = np.zeros(2)
    directions = [1, 7, 6, 8]
    for pl in [player, 1-player]:
        for d in directions:
            bb = state.boards[pl] & (state.boards[pl] >> d)
            if bb != 0:
                scores[pl] += 0.05
            if bb & (state.boards[pl] >> 2*d)!= 0:
                scores[pl] += 0.1

    return scores[player] - scores[1 - player]


def cutoff_test(game, state, depth, max_depth):
    if game.terminal_test(state):
        return True
    if state.counter > 8 and depth > max_depth:
        return True
    return False

    