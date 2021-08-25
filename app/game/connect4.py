from game.game_state import GameState

class Connect4:
    def __init__(self, width=7, height=6, connect=4):
        self.width = width
        self.height = height
        self.connect = connect
        self.initial = GameState()


    def make_move(self, state, column):
        move = 1 << state.height[column]
        state.boards[state.counter & 1] ^= move
        state.moves.append(column)
        state.height[column] += 1
        state.counter += 1


    def undo_move(self, state):
        column = state.moves.pop()
        state.counter -= 1
        state.height[column] -= 1
        move = 1 << state.height[column]
        state.boards[state.counter & 1] ^= move


if __name__ == '__main__':
    game = Connect4()
    state = game.initial
    state.display()
    game.make_move(state, 2)
    state.display()
    game.make_move(state, 2)
    state.display()
    game.make_move(state, 3)
    state.display()
    game.make_move(state, 4)
    state.display()
    game.make_move(state, 0)
    state.display()
    
