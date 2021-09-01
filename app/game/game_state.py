from collections import deque
import numpy as np


class GameState:
    def __init__(self):
        self.boards = [0, 0]
        self.height = np.array([0, 7, 14, 21, 28, 35, 42], dtype=np.uint)
        self.counter = 0
        self.moves = deque() 
        self.utility = 0
    

    def as_string(self, player):
        return "{:b}".format(self.boards[player % 2]).zfill(49)


    def _board(self, player):
        return np.rot90(np.array(list(self.as_string(player)), dtype=int).reshape(7, 7), k=3)


    def as_board(self):
        return self._board(0)[1:, :] - self._board(1)[1:, :]
    
    
    def display(self):
        board = self.as_board()
        for row in board:
            for el in row:
                if el == 0:
                    print('.', end=' ')
                elif el == 1:
                    print('X', end=' ')
                else:
                    print('O', end=' ')
            print()
        print()

    
    def __hash__(self):
        return hash(tuple(self.boards))
                
      