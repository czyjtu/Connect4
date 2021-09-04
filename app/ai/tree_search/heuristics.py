import numpy as np
from scipy.signal import convolve2d
from numba import njit


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
            bb2 = bb & (state.boards[pl] >> 2*d)
            if bb2 != 0:
                scores[pl] += 0.1
            if bb2 & (state.boards[pl] >> 3*d):
                scores[pl] += 1
    return scores[player] - 2*scores[1 - player]

horizontal_kernel = np.array([[ 1, 1, 1, 1]])
vertical_kernel = np.transpose(horizontal_kernel)
diag1_kernel = np.eye(4, dtype=np.uint8)
diag2_kernel = np.fliplr(diag1_kernel)
detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]


def eval_fun_1(game, state, player, ):
    board = state.as_board()
    pl_4 = 0
    pl_3 = 0
    op_4 = 0
    op_3 = 0
    pl = 1 if player == 0 else -1
    for kernel in detection_kernels:
        conv = convolve2d(board == pl, kernel, mode="valid")
        # conv_op = convolve2d(board == -pl, kernel, mode="valid")
        pl_3 += np.count_nonzero(conv == 3)
        # pl_4 += np.count_nonzero(conv == 4)
        op_3 += np.count_nonzero(conv == -3)
    # print(pl_4, pl_3, op_4, op_3)
    return pl_4 or -op_4 or 1e-4*pl_3 - 1e-4*op_3


def eval_fun_data(game, state, player, lookup_table, local_lookup):
    v=0
    u = game.compute_utility(state)
    if u != 0:
        state.utility = u
        return 2*u if player == 0 else -2*u
    if tuple(state.boards) in local_lookup:
        return local_lookup[tuple(state.boards)]
    if tuple(state.boards) in lookup_table:
        v = lookup_table[tuple(state.boards)] if player == 0 else -lookup_table[tuple(state.boards)]
        if v == 1: return v
        if v == 0: return 0.1

    board = state.as_board()
    pl_4 = 0
    pl_3 = 0
    op_4 = 0
    op_3 = 0
    pl = 1 if player == 0 else -1
    for kernel in detection_kernels:
        conv = convolve2d(board == pl, kernel, mode="valid")
        pl_3 += np.count_nonzero(conv == 3)
        op_3 += np.count_nonzero(conv == -3)
    score = pl_4 or -op_4 or 0.5*pl_3 - 0.1*op_3
    local_lookup[tuple(state.boards)] = score + v
    return score + v




    