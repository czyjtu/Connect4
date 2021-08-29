import numpy as np


def minmax(game, state):
    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            game.make_move(state, a)
            v = max(v, min_value(state))
            game.undo_move(state)
        return v

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
        if len(state.moves) == 8 and tuple(state.boards) in utilities:
            u = utilities[tuple(state.boards)]
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
        if len(state.moves) == 8 and tuple(state.boards) in utilities:
            u = utilities[tuple(state.boards)]
            return u if player == 0 else - u
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
