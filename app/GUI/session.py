from game.connect4 import Connect4
from GUI.board import Board
import pygame


class Session:
    SCREEN_SIZE = (720, 720)
    BACKGROUND_COL = (82, 92, 108)

    def __init__(self, population_size=10):
        pygame.init()
        self.screen = pygame.display.set_mode(Session.SCREEN_SIZE)
        self.board = Board(Session.SCREEN_SIZE)
        self.ai_player_id = 1
        self.clock = pygame.time.Clock()
        self.running = True


    def render(self):
        self.screen.fill(Session.BACKGROUND_COL)
        self.board.render(self.screen)
        pygame.display.flip()


    def update(self):
        if self.board.is_finished():
            self.cleanup()
        if self.board.get_turn() == self.ai_player_id:
            self.board.update()


    def keep_fps(self, fps=60.0):
        self.clock.tick(fps)
    

    def handle_events(self, navigation=True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                if self.board.get_turn() != self.ai_player_id:
                    col = self.board.get_column(posx)
                    self.board.drop_chip(col)


    def cleanup(self):
        pygame.quit()