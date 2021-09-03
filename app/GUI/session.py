from game.connect4 import Connect4
from GUI.board import Board
import pygame


class Session:
    SCREEN_SIZE = (720, 720)
    BACKGROUND_COL = (82, 92, 108)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Session.SCREEN_SIZE)
        self.new_game()


    def new_game(self):
        self.board = Board(Session.SCREEN_SIZE)
        self.ai_player_id = 1
        self.clock = pygame.time.Clock()
        self.running = True


    def render(self):
        if self.board.finished:
            self._end_screen()
        else:
            self._game_screen()


    def _start_screen(self):
        pass


    def _game_screen(self):
        self.screen.fill(Session.BACKGROUND_COL)
        self.board.render(self.screen)
        pygame.display.flip()


    def _end_screen(self):
        self.screen.fill(Session.BACKGROUND_COL)
        self.board._render_end_game(self.screen)
        pygame.display.flip()


    def update(self):
        if self.board.get_turn() == self.ai_player_id and not self.board.finished:
            self.board.update()


    def keep_fps(self, fps=30.0):
        self.clock.tick(fps)
    

    def handle_events(self, navigation=True):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.new_game()
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                if self.board.get_turn() != self.ai_player_id:
                    col = self.board.get_column(posx)
                    self.board.drop_chip(col)


    def cleanup(self):
        # display 
        pygame.quit()