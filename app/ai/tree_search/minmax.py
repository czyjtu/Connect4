import numpy as np


def minmax(game, state, max_depth=10, lookup_table={}, dataset={}):
    def minmax_decision(state, maximizing):
        # if state in lookup_table:
        #     v = lookup_table[state]
        #     return v if player == 0 else -v
        if state.counter > max_depth:
            return -np.inf if maximizing else np.inf
        if game.terminal_test(state):
            game.compute_utility(state)
            return game.compute_utility(state)
        
        ###--use of datasets--###
        if state.counter == 8:
            if tuple(state.boards) in dataset:
                u = dataset[tuple(state.boards)]
                return u if player == 0 else -u
            # check if the player can win in next move
            current_player = state.counter & 1
            if game.get_winning(state, current_player) is not None:
                return 1 if player == current_player else -1
            # check if the oponent have winning move
            move = game.get_winning(state, 1 - current_player)
            if move is not None:
                # make move to prevent other player winning
                game.make_move(state, move)
                v = minmax_decision(state, not maximizing)
                game.undo_move(state)
                return v
            state.display()
            raise ValueError
        ###-------------------###
        best = -np.inf if maximizing else np.inf
        cutoff = 1 if maximizing else -1
        for a in game.actions(state):
            game.make_move(state, a)
            value = minmax_decision(state, not maximizing)
            best = max(best, value) if maximizing else min(best, value) 
            game.undo_move(state)
            if best == cutoff: 
                lookup_table[state] = best if player == 0 else -best
                break
        return best

    player = state.counter & 1
    move = game.get_winning(state, player)
    if move:
        return move
    actions = game.actions(state)
    best_action = None
    best_utility = -np.inf
    for action in actions:
        game.make_move(state, action)
        utility = minmax_decision(state, False)
        game.undo_move(state)
        print(f"depth {max_depth} -> ({action}, {utility})")
        if utility == 1:
            return action
        if utility > best_utility and -3 < utility < 3:
            best_utility = utility
            best_action = action
    if best_utility == 0:
        return best_action
    elif abs(best_utility) != np.inf:
        return np.random.choice(actions)

    return None


def idminmax(game, state, utilities, max_depth=22, lookup_table={}):
    for depth in range(8, max_depth + 1):
        print("depth", depth)
        a = minmax(game, state, dataset=utilities, max_depth=depth, lookup_table=lookup_table)
        if a is not None:
            return a

