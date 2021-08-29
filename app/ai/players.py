from ai.tree_search.minmax import minmax, minmax_data
import numpy as np

def random_player(game, state):
    actions = game.actions(state)
    return np.random.choice(actions) if actions else None


def minmax_player(game, state):
    return minmax(game, state)


def minmax_player_data(game, state, utilities):
    return minmax_data(game, state, utilities)