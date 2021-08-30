from ai.tree_search.minmax import minmax, idminmax
from timeit import default_timer as timer
import numpy as np


def timeit_decorator(function):
    def wraper(*args, **kwargs):
        s = timer()
        result = function(*args, **kwargs)
        e = timer()
        print(f"{function.__name__} call took: {e-s} [s]")
        return result
    return wraper


@timeit_decorator
def random_player(game, state):
    actions = game.actions(state)
    return np.random.choice(actions) if actions else None


@timeit_decorator
def minmax_player(game, state, data):
    return minmax(game, state, dataset=data)


@timeit_decorator
def idminmax_player(game, state, data, lookup_table={}):
    return idminmax(game, state, data, 8, lookup_table=lookup_table)