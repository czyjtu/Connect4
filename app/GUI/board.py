from ai.players import idminmax_player
from game import Connect4

import pygame
from pygame import gfxdraw
import pickle   


class Board:
    CHIP_RADIUS = 0.4 # 90% of the column width
    CHIP_OFFSET = 0.1 # 10% of the column width
    PLAYER_COL = {1: (82, 212, 212) , -1: (255, 195, 0 ), 0: (157, 168, 187)}


    def __init__(self, screen_size):
        self.sz = screen_size
        self.COL_WIDTH = screen_size[1] / 7
        self.ROW_HEIGHT = screen_size[0] / 7
        self.game = Connect4()
        self.state = self.game.initial
        self.finished = False
        with open("data/8ply.pkl", "rb") as f:
            data = pickle.load(f)
        self.ai_player = lambda *args: idminmax_player(*args, lookup_table=data)


    def update(self):
        a = self.ai_player(self.game, self.state)
        print(f"ai move: {a}")
        self._ply(a)


    def render(self, screen):
        for row, spots in enumerate(self.state.as_board()):
            for column, spot in enumerate(spots):
                gfxdraw.aacircle(
                    screen,
                    int(0.5*self.COL_WIDTH + column*self.COL_WIDTH), int(1.5*self.ROW_HEIGHT + row*self.ROW_HEIGHT), 
                    int(Board.CHIP_RADIUS*self.COL_WIDTH),  Board.PLAYER_COL[spot]
                )
                gfxdraw.filled_circle(
                    screen, 
                    int(0.5*self.COL_WIDTH + column*self.COL_WIDTH), int(1.5*self.ROW_HEIGHT + row*self.ROW_HEIGHT), 
                    int(Board.CHIP_RADIUS*self.COL_WIDTH),  Board.PLAYER_COL[spot]
                )


    def get_column(self, posx):
        print(posx, self.COL_WIDTH)
        col = int(posx // self.COL_WIDTH)
        print(f"player move: {col}")
        return col


    def get_turn(self):
        return self.state.counter & 1


    def drop_chip(self, col):
        if col in self.game.actions(self.state):
            self._ply(col)


    def _render_end_game(self, screen):
        result = {
            1: "PLAYER 1 WON",
            0: "DRAW",
            -1: "PLAYER 2 WON"
        }
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        
        textsurface = myfont.render(f'GAME OVER: {result[self.state.utility]}', False, (0, 0, 0))
        screen.blit(textsurface,(0,0))


    def _ply(self, col):
        if not self.finished:
            self.game.make_move(self.state, col)
        if self.game.terminal_test(self.state):
            u = self.state.utility
            self.finished = True
            print("utility", u)
            return u


    def clear(self):
        pass