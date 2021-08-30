import numpy as np
from functools import lru_cache

def minmax(game, state):
    @lru_cache
    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            game.make_move(state, a)
            v = max(v, min_value(state))
            game.undo_move(state)
        return v

    @lru_cache
    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            game.make_move(state, a)
            v = min(v, max_value(state))
            game.undo_move(state)
        return v

    player = state.counter & 1
    actions = game.actions(state)
    best_action = None
    best_utility = -np.inf
    for action in actions:
        game.make_move(state, action)
        utility = min_value(state)
        game.undo_move(state)
        print(action, utility)
        if utility == 1: # winning move
            return action
        if utility > best_utility:
            best_utility = utility
            best_action = action
        # print(action, utility)
    return best_action
    # return max(game.actions(state), key=lambda a: min_value(game.result(state, a)))


def minmax_data(game, state, utilities):

    def max_value(state):
        if len(state.moves) == 8:
            if tuple(state.boards) in utilities:
                u = utilities[tuple(state.boards)]
            else:
                move, u = game.get_forced(state)
                if move is not None:
                    return u if player == 0 else -u
                else:
                    state.display()
                    print(state.moves)
                    print(state.boards)
                    print(state.counter)
                    raise ValueError
            return u if player == 0 else - u
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            game.make_move(state, a)
            v = max(v, min_value(state))
            game.undo_move(state)
        return v


    def min_value(state):
        if len(state.moves) == 8:
            if tuple(state.boards) in utilities:
                u = utilities[tuple(state.boards)]
            else:
                move, u = game.get_forced(state)
                if move is not None:
                    return u if player == 0 else -u
                else:
                    state.display()
                    # state.display()
                    print(state.moves)
                    print(state.boards)
                    print(state.counter)
                    raise ValueError
            return u if player == 0 else - u
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            game.make_move(state, a)
            v = min(v, max_value(state))
            game.undo_move(state)
        return v

    
    move, u = game.get_forced(state)
    if move:
        return move
    player = state.counter & 1
    actions = game.actions(state)
    best_action = None
    best_utility = -np.inf
    for action in actions:
        game.make_move(state, action)
        utility = min_value(state)
        game.undo_move(state)
        print(action, utility)
        if utility == 1: # winning move
            return action
        if utility > best_utility:
            best_utility = utility
            best_action = action
        # print(action, utility)
    return best_action
