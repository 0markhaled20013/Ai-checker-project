import pygame
import sys
from pygame.locals import *
from constants import *
from game import Game

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Checkers')
    clock = pygame.time.Clock()
    game = Game(win)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN and game.turn == RED_P and not game.board.winner():
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                game.select(row, col)

        if game.turn == BLACK_P and not game.board.winner():
            game.ai_move()

        game.update()

if __name__ == "__main__":
    main()
