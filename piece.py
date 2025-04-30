import pygame
from constants import SQUARE_SIZE, RED, BLACK, CROWN, RED_P, RED_K

class Piece:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - 10
        pygame.draw.circle(win, RED if self.color in (RED_P, RED_K) else BLACK, (self.x, self.y), radius)
        if self.king:
            pygame.draw.circle(win, CROWN, (self.x, self.y), radius // 2)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
