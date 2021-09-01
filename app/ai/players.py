from ai.tree_search.minmax import minmax, idminmax
from timeit import default_timer as timer
from ai.tree_search.heuristics import eval_fun_0, cutoff_test
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
def minmax_player(game, state, lookup_table={}):
    return minmax(game, state, lookup_table=lookup_table)


@timeit_decorator
def idminmax_player(game, state, lookup_table={}):
    return idminmax(game, state, max_depth=8, lookup_table=lookup_table, eval_fun=eval_fun_0, cutoff_test=lambda *args: cutoff_test(*args, max_depth=6))


@timeit_decorator
def query_player(game, state):
    print(f"possible actions: {game.actions(state)}")
    a = int(input("action: "))
    return a