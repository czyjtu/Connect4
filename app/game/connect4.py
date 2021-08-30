from game.game_state import GameState
import numpy as np

class Connect4:
    def __init__(self, width=7, height=6, connect=4):
        self.width = width
        self.height = height
        self.connect = connect
        self.initial = GameState()


    def make_move(self, state, column, player=None):
        # print(f"{player} ({state.counter & 1}) - make -> {column}")
        if player is None:
            player = state.counter & 1
        move = 1 << state.height[column]
        state.boards[player] ^= move
        state.moves.append(column)
        state.height[column] += 1
        state.counter += 1
        state.utility = self.compute_utility(state)


    def undo_move(self, state, player=None):
        column = state.moves.pop()
        # print(f"{player} ({state.counter & 1}) - pop -> {column}")
        state.counter -= 1
        if player is None:
            player = state.counter & 1
        state.height[column] -= 1
        move = 1 << state.height[column]
        state.boards[player] ^= move


    def actions(self, state):
        moves = []
        top = int('1000000100000010000001000000100000010000001000000', 2)
        for m in range(7):
            if top & (1 << state.height[m]) == 0:
                moves.append(m)
        return moves

    
    def terminal_test(self, state):
        return len(self.actions(state)) == 0 or self.is_win(state, 1 - state.counter & 1)


    def utility(self, state, player):
        return state.utility if player == 0 else - state.utility


    def compute_utility(self, state):
        if self.is_win(state, 0):
            return 1
        if self.is_win(state, 1):
            return -1
        return 0


    def is_win(self, state, player):
        directions = [1, 7, 6, 8]
        for d in directions:
            bb = state.boards[player] & (state.boards[player] >> d)
            if (bb & (bb >> (2 * d))) != 0:
                return True
        return False


    def get_forced(self, state):
        if state.counter < 6:
            return None, None
        if state.counter & 1 == 0:
            order = [0, 1]
        else:
            order = [1, 0]
        for player in order:
            for a in self.actions(state):
                self.make_move(state, a, player)
                winning = self.is_win(state, player)
                self.undo_move(state, player)
                if winning:
                    return (a, 1) if player == 0  else (a, -1)
        return None, None

    
    def play_game(self, *players):
        state = self.initial
        while True:
            for i, player in enumerate(players):
                if self.terminal_test(state):
                    print(state.utility)
                    return 
                m = player(self, state)
                print(f"player {i} -> {m}")
                self.make_move(state, m)
                state.display()
            


if __name__ == '__main__':
    game = Connect4()
    state = game.initial
    state.display()
    game.make_move(state, 5)
    state.display()
    game.make_move(state, 2)
    state.display()
    game.make_move(state, 3)
    state.display()
    game.make_move(state, 4)
    state.display()
    game.make_move(state, 0)
    state.display()
    # game.play_game()
