from ai.tree_search.minmax import minmax, idminmax
from timeit import default_timer as timer
from ai.tree_search.heuristics import eval_fun_1, eval_fun_data
from ai.tree_search.mcts import MCTS
import numpy as np
import pickle


def timeit_decorator(function):
    def wraper(*args, **kwargs):
        s = timer()
        result = function(*args, **kwargs)
        e = timer()
        print(f"{function.__name__} call took: {e-s} [s]")
        return result
    return wraper



class MinmaxPlayer:
    def __init__(self, game, path=None, eval_fun=eval_fun_data, max_depth=6):
        self.game = game
        self.eval_fun = eval_fun
        self.max_depth = max_depth
        self.data = self.load_data(path)
    

    def load_data(self, path):
        data = {}
        if path:
            with open(path, "rb") as f:
                data = pickle.load(f)
            return data

    @timeit_decorator
    def next_move(self, state): 
        return minmax(self.game, state, lookup_table=self.data, max_depth=self.max_depth, eval_fun=self.eval_fun)
        


class MctsPlayer:
    def __init__(self, game, path=None):
        self.game = game
        self.mcts = self.load_mcts(path)
    

    def load_mcts(self, path):
        if path:
            with open(path, "rb") as f:
                root = pickle.load(f)
            mcts = MCTS(self.game, self.game.initial, root)
        else:
            mcts = MCTS(self.game, self.game.initial)
            mcts.train(1000)
        return mcts

    @timeit_decorator
    def next_move(self, state):
        move, subtree = self.mcts.new_ply(state, rollouts=1000)
        self.mcts = subtree
        return move