import numpy as np

class Node:
    def __init__(self, parent=None, state=None, U=0, N=0):
        self.parent=parent,
        self.state=state,
        self.U=U,
        self.N=N
        self.children = {}
        self.actions = None

    def __hash__(self):
        return hash(tuple(self.state.boards))


def ucb(n, C=1.4):
    return np.inf if n.N == 0 else n.U / n.N + C * np.sqrt(np.log(n.parent.N) / n.N)


class MCTS:
    def __init__(self, game, state, root=None, N=1000):
        self.root = root or Node(state=state)
        self.N = N
        self.nodes = set(self.root)

    
    def choose_child(self, node, fitness=lambda p: p.N):
        """choose best child according to fitness function"""
        return max(node.children.keys(), key=fitness)
    

    def _select(self, node):
        """select a leaf"""
        return self.select(self.choose_child(node, fitness=ucb)) if node.children else node

    
    def _expand(self, node):
        """add available actions (childrens) to the leaf node"""
        pass

    def _simulate(self, node):
        """play random game till the end and return reward"""
        pass 


    def _backpropagate(self, reward):
        """propagate the reward upward the tree, and update every node"""
        pass


    def train(self, epochs):
        """pretrain tree for given number of epochs"""
        pass
        
