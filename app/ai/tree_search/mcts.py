import numpy as np
from game.connect4 import Connect4
from game.game_state import GameState

class Node:
    def __init__(self, state=None, parent=None, reward=0, visits=0):
        self.parent=parent
        self.state=state
        self.reward=reward
        self.visits=visits
        self.children = {}
        self.actions = None

    def __hash__(self):
        return hash(tuple(self.state.boards))

    def __str__(self):
        return f"|boards:{self.state.boards}, action: {self.parent.children[self] if self.parent else None}|"


def ucb(node, C=1.4):
    return np.inf if node.visits == 0 else node.reward / node.visits + C * np.sqrt(np.log(node.parent.visits) / node.visits)
    

class MCTS:
    def __init__(self, game, state, root=None, N=1000):
        self.root = root or Node(state=state)
        self.N = N
        self.nodes = set([self.root])
        self.game = game

    
    def choose_child(self, node, fitness=lambda p: p.N):
        """choose best child according to fitness function"""
        return max(node.children.keys(), key=fitness)
    

    def _select(self, node):
        """select a leaf"""
        return self._select(self.choose_child(node, fitness=ucb)) if node.children else node

    
    def _expand(self, node):
        """add available actions (childrens) to the leaf node"""
        if node.children:
            raise ValueError("Given Node already has children. Cannot expand it further")
        if not self.game.terminal_test(node.state):
            node.children = {
                Node(parent=node, state=self.game.result(node.state, move)): move
                for move in self.game.actions(node.state) 
            }
            self.nodes.update(node.children.keys())


    def _simulate(self, node):
        """play random game till the end and return reward"""
        state = node.state
        player = state.counter & 1
        while not self.game.terminal_test(state):
            move = np.random.choice(self.game.actions(state))
            state = self.game.result(state, move)
        u = self.game.compute_utility(state)
        return u if player == 0 else -u


    def _backpropagate(self, node, reward, root=None):
        """propagate the reward upward the tree, and update every node"""
        node.visits += 1
        if reward > 0: 
            node.reward += reward # increment number of wins
        if node.parent is not None or node == root: # propagate until root of the tree or given terminal node is reached
            self._backpropagate(node.parent, -reward)


    def rollout(self, root):
        leaf = self._select(root)
        self._expand(leaf)
        child = self._select(leaf) # child or node if node is terminal
        reward = self._simulate(child)
        self._backpropagate(child, reward, root)


    def train(self, epochs, root=None):
        """rollout tree from the given root, for the given number of epochs"""
        root = root or self.root
        for _ in range(epochs):
            self.rollout(root)


    def decide(self, state, rollouts=1000):
        pass
        


        
if __name__ == '__main__':
    game = Connect4()
    st = game.initial
    mcts = MCTS(game, state=st)
    print(*mcts.nodes)
    mcts.train(100)
    print(*mcts.nodes)



        
