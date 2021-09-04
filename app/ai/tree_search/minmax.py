import numpy as np


def minmax(game, state, max_depth=8, lookup_table={}, eval_fun=None, cutoff_test=None, order_actions=None):
    def minmax_decision(state, maximizing, depth, alpha, beta):
        if cutoff_test(game, state, depth):
            return eval_fun(game, state, player,lookup_table, local_lookup)
        to_explore = order_actions(game, state, player)
        best = -np.inf if maximizing else np.inf
        for a in to_explore:
            game.make_move(state, a)
            value = minmax_decision(state, not maximizing, depth + 1, alpha, beta)
            best = max(best, value) if maximizing else min(best, value) 
            game.undo_move(state)
            if maximizing:
                if best >= beta:
                    break
                alpha = max(alpha, best)
            else:
                if best <= alpha:
                    break
                beta = max(beta, best)
        return best
    if state.height[3] == 21: # go for center if it is empty
        return 3
    local_lookup = dict() # create lookup table not to repeat calculations 
    player = state.counter & 1
    max_depth = 9 - state.counter if 8 - state.counter > max_depth and len(lookup_table) > 0 else max_depth
    cutoff_test = (cutoff_test or (lambda game, state, depth: depth > max_depth or game.terminal_test(state)))
    eval_fun = eval_fun or (lambda game, state, player: game.utility(state, player))
    order_actions = order_actions or (lambda g, s, p: g.get_winning(s, p) or g.get_winning(s, 1 - p) or sorted(g.actions(s), key=lambda x: abs(x-3)))
    to_explore = order_actions(game, state, player)
    best_utility = -np.inf
    best_action = None
    beta = np.inf
    for action in to_explore:
        game.make_move(state, action)
        utility = minmax_decision(state, False, 1, best_utility, beta)
        game.undo_move(state)
        print(f"depth {max_depth} -> ({action}, {utility})")
        if utility >= beta:
            print(len(local_lookup))
            return action
        if utility > best_utility:
            best_utility = utility
            best_action = action
    return best_action


def idminmax(game, state, max_depth, lookup_table={}, eval_fun=None, cutoff_test=None):
    for depth in range(1, max_depth + 1):
        print("depth", depth)
        a = minmax(game, state, max_depth=depth, lookup_table=lookup_table, eval_fun=eval_fun, cutoff_test=cutoff_test)
        if a is not None:
            return a




