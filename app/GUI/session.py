from game.connect4 import Connect4
from GUI.board import Board
from GUI.button import Button
import pygame
import enum 
pygame.font.init()


class Session:
    SCREEN_SIZE = (512, 512)
    BACKGROUND_COL = (82, 92, 108)
    FONT = pygame.font.Font(None,30)
    FONT_COL = '#FFFFFF'
    mode = enum.Enum('Mode', 'START, GAME, ENDGAME')

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Session.SCREEN_SIZE)
        self.grid_w = Session.SCREEN_SIZE[0] // 8
        self.grid_h = Session.SCREEN_SIZE[1] // 10
        b_w = 2 * self.grid_w
        b_h = self.grid_h
        self.button_player = Button('Me first', b_w, b_h, (self.grid_w, 2*self.grid_h), 5)
        self.button_ai = Button('AI first', b_w, b_h, (5*self.grid_w, 2*self.grid_h), 5)
        self.running = True
        self.new_game()


    def new_game(self):
        self.mode = Session.mode.START
        self.board = Board(Session.SCREEN_SIZE)
        self.ai_player_id = None # clik to set it up
        self.clock = pygame.time.Clock()


    def render(self):
        self.screen.fill(Session.BACKGROUND_COL)
        if self.mode == Session.mode.START:
            self._start_screen()
        elif self.mode == Session.mode.ENDGAME:
            self._end_screen()
        else:
            self._game_screen()
        pygame.display.flip()


    def _start_screen(self):
        textsurface = Session.FONT.render(f"WHO'S FIRST?", True, Session.FONT_COL)
        self.screen.blit(textsurface,(3*self.grid_w, self.grid_h))
        self.button_player.draw(self.screen)
        self.button_ai.draw(self.screen)
          

    def _game_screen(self):
        self.board.render_game(self.screen)


    def _end_screen(self):
        textsurface = Session.FONT.render(f'GAME OVER', True, Session.FONT_COL)
        self.screen.blit(textsurface, (3*self.grid_w, self.grid_h // 4))
        textsurface = Session.FONT.render(f"PRESS 'R' TO RESTART", True, Session.FONT_COL)
        self.screen.blit(textsurface, (int(2.2*self.grid_w), self.grid_h))
        self.board.render_endgame(self.screen)


    def update(self):
        if self.board.get_turn() == self.ai_player_id and not self.board.finished:
            self.board.update()


    def keep_fps(self, fps=30.0):
        self.clock.tick(fps)
    

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.mode == Session.mode.START:
                self._start_events(event)
            elif self.mode == Session.mode.GAME:
                self._game_events(event)
            elif self.mode == Session.mode.ENDGAME:
                self._endgame_events(event)


    def _start_events(self, event):
        pressed = False
        if self.button_player.pressed:
            self.button_player.pressed = False
            pressed = True
            self.ai_player_id = 1
        elif self.button_ai.pressed:
            self.button_ai.pressed = False
            pressed = True
            self.ai_player_id = 0
        self.mode = Session.mode.GAME if pressed else self.mode

    
    def _game_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.new_game()
        if event.type == pygame.MOUSEBUTTONDOWN:
            posx = event.pos[0]
            if self.board.get_turn() != self.ai_player_id:
                col = self.board.get_column_from_pos(posx)
                self.board.drop_chip(col)
        self.mode = Session.mode.ENDGAME if self.board.finished else self.mode


    def _endgame_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.new_game()


    def cleanup(self):
        self.running = False
        pygame.quit()