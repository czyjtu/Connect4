from ai.players import minmax_player
from game import Connect4
import pygame
from pygame import gfxdraw
import pickle   
import numpy as np
from scipy.signal import convolve2d



class Board:
    CHIP_RADIUS = 0.4 # 90% of the column width
    CHIP_OFFSET = 0.1 # 10% of the column width
    PLAYER_COL = {1: (215, 75, 75) , -1: (255, 195, 0 ), 0: (157, 168, 187)}


    def __init__(self, screen_size):
        self.sz = screen_size
        self.COL_WIDTH = screen_size[1] / 7
        self.ROW_HEIGHT = screen_size[0] / 7
        self.game = Connect4()
        self.state = self.game.initial
        self.finished = False
        with open("data/8ply.pkl", "rb") as f:
            data = pickle.load(f)
        self.ai_player = lambda *args: minmax_player(*args, lookup_table=data)
        self.ply_num = 0
        
        horizontal_kernel = np.array([[ 1, 1, 1, 1]])
        vertical_kernel = np.transpose(horizontal_kernel)
        diag1_kernel = np.eye(4, dtype=np.uint8)
        diag2_kernel = np.fliplr(diag1_kernel)
        self.detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]
        self.kernel_direct = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        self.waiting_for_move = False


    def update(self):
        self._ply(self.ai_player(self.game, self.state))


    def _render_chip(self, screen, row, column, colour):
        gfxdraw.aacircle(
            screen,
            int(0.5*self.COL_WIDTH + column*self.COL_WIDTH), int(1.5*self.ROW_HEIGHT + row*self.ROW_HEIGHT), 
            int(Board.CHIP_RADIUS*self.COL_WIDTH),  colour
        )
        gfxdraw.filled_circle(
            screen, 
            int(0.5*self.COL_WIDTH + column*self.COL_WIDTH), int(1.5*self.ROW_HEIGHT + row*self.ROW_HEIGHT), 
            int(Board.CHIP_RADIUS*self.COL_WIDTH), colour
        )


    def _render_board(self, screen, winning_chips=set()):
        for row, spots in enumerate(self.state.as_board()):
            for column, spot in enumerate(spots):
                alpha = 255 if (len(winning_chips) == 0 or (row, column) in winning_chips) else 100
                self._render_chip(screen, row, column, (*Board.PLAYER_COL[spot], alpha))


    def render_endgame(self, screen):
        result = {1: "PLAYER 1 WON", 0: "DRAW", -1: "PLAYER 2 WON"}
        winning_chips = self._get_winning_chips()
        self._render_board(screen, winning_chips)


    def render_game(self, screen):
        self._render_board(screen)


    def get_column_from_pos(self, posx):
        print(posx, self.COL_WIDTH)
        col = int(posx // self.COL_WIDTH)
        print(f"player move: {col}")
        return col


    def get_turn(self):
        return self.state.counter & 1


    def drop_chip(self, col):
        if col in self.game.actions(self.state):
            self._ply(col)

    
    def _get_winning_chips(self):
        board = self.state.as_board()
        for player in [-1, 1]:
            for i, kernel in enumerate(self.detection_kernels):
                conv = convolve2d(board == player, kernel, mode="valid")
                if (conv== 4).any():
                    where_row, where_col = np.where(conv == 4)
                    r, c = where_row[0], where_col[0]
                    if i == 3: #poositive diagonal treated differenty
                        r += 3 # left bottom corner of the kernel
                    dir = self.kernel_direct[i]
                    idxs = [(r + j*dir[0], c + j*dir[1]) for j in range(4)]
                    return set(idxs)
        return set()


    def undo_last_ply(self):
        self.game.undo_move(self.state)


    def _ply(self, col):
        if not self.finished:
            self.ply_num += 1
            self.game.make_move(self.state, col)
        if self.game.terminal_test(self.state):
            u = self.state.utility
            self.finished = True
            print("utility", u)
            return u


    def clear(self):
        pass