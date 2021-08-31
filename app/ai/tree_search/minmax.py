import numpy as np


def minmax(game, state, max_depth=10, lookup_table={}, eval_fun=None, cutoff_test=None, order_actions=None):
    def minmax_decision(state, maximizing, depth, alpha, beta):
        if tuple(state.boards) in lookup_table:
            v = lookup_table[tuple(state.boards)]
            return v if player == 0 else -v
        if cutoff_test(state, depth):
            return eval_fun(game, state, player)
        to_explore = order_actions(game, state, player)
        best = -np.inf if maximizing else np.inf
        for a in to_explore:
            game.make_move(state, a)
            value = minmax_decision(state, not maximizing, depth + 1, alpha, beta)
            best = max(best, value) if maximizing else min(best, value) 
            game.undo_move(state)
            if maximizing:
                if best >= beta:
                    lookup_table[tuple(state.boards)] = best if player == 0 else -best
                    break
                alpha = max(alpha, best)
            else:
                if best <= alpha:
                    lookup_table[tuple(state.boards)] = best if player == 0 else -best
                    break
                beta = max(beta, best)
        return best

    player = state.counter & 1
    cutoff_test = (cutoff_test or (lambda state, depth: depth > max_depth or game.terminal_test(state)))
    eval_fun = eval_fun or (lambda game, state, player: game.utility(state, player))
    order_actions = order_actions or (lambda g, s, p: g.get_winning(s, p) or g.get_winning(s, 1 - p) or g.actions(s))
    to_explore = order_actions(game, state, player)
    best_utility = -1
    best_action = None
    beta = 1
    for action in to_explore:
        game.make_move(state, action)
        utility = minmax_decision(state, False, 1, best_utility, beta)
        game.undo_move(state)
        print(f"depth {max_depth} -> ({action}, {utility})")
        if utility >= beta:
            return action
        if utility > best_utility:
            best_utility = utility
            best_action = action
   
    if abs(best_utility) != np.inf:
        return np.random.choice(to_explore)

    return best_action


def idminmax(game, state, max_depth=22, lookup_table={}, eval_fun=None):
    for depth in range(8, max_depth + 1):
        print("depth", depth)
        a = minmax(game, state, max_depth=depth, lookup_table=lookup_table, eval_fun=eval_fun)
        if a is not None:
            return a

