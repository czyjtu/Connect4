import numpy as np
from game.connect4 import Connect4
from game.game_state import GameState
from copy import deepcopy
import pickle
from tqdm import tqdm


class Node:
    def __init__(self, state=None, parent=None, reward=0, visits=0):
        self.parent=parent
        self.state=state
        self.reward=reward
        self.visits=visits
        self.children = {}
        self.actions = None

    def __hash__(self):
        return self.state.__hash__()

    def __str__(self):
        return f"|boards:{self.state.boards}, action: {self.parent.children[self] if self.parent else None}|"


def ucb(node, C=1.5):
    return np.inf if node.visits == 0 else node.reward / node.visits + C * np.sqrt(np.log(node.parent.visits) / node.visits)
    

class MCTS:
    def __init__(self, game, state, root=None):
        state = deepcopy(state)
        self.root = root or Node(state=state)
        self.nodes = MCTS.register_tree_nodes(self.root)
        self.game = game
        self.expanded = 0


    @staticmethod
    def register_tree_nodes(root):
        """Traverse the tree starting from root, and register visited nodes"""
        def traverse(n):
            nonlocal all_nodes
            for child in n.children.keys():
                all_nodes[child.state] = child
                traverse(child)
        all_nodes = {root.state: root}
        traverse(root)
        return all_nodes


    def choose_child(self, node, fitness=lambda p: p.visits):
        """choose best child according to fitness function"""
        return max(node.children.keys(), key=fitness)

    
    def choose_action(self, node=None):
        node = node or self.root
        best_child = self.choose_child(node)
        return node.children[best_child]
    

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
            self.nodes.update({n.state: n for n in node.children.keys()})


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
        self._backpropagate(child, -reward, root)


    def train(self, epochs, root=None, path=None):
        """rollout tree from the given root, for the given number of epochs"""
        root = root or self.root
        for _ in tqdm(range(epochs)):
            self.rollout(root)
        if path:
            with open(path, "wb") as f:
                pickle.dump(self, f)


    def new_ply(self, state, rollouts=1600):
        """
        cutoff the subtree coresponding to the given state, 
        do some rollouts and return best action along wth the new tree
        """
        sub_tree = None
        if state not in self.nodes: # create completly new tree
            sub_tree = MCTS(self.game, state)
        else:
            print("new tree created")
            new_root = self.nodes[state] # reuse node from current tree with precomputed information
            sub_tree = MCTS(self.game, state, root=new_root)

        sub_tree.train(rollouts)
        goal_move = sub_tree.choose_action()
        return goal_move, sub_tree

