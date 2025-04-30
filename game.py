import pygame
from constants import *
from board import Board
from ai import minimax

class Game:
    def __init__(self, win):
        self.win = win
        self.board = Board()
        self.turn = RED_P
        self.valid_moves = {}
        self.selected = None
        self.ai_thinking = False
        self.font = pygame.font.SysFont('Arial', 30)

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves()
        if self.selected:
            row, col = self.selected
            pygame.draw.rect(self.win, BLUE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

        if self.board.winner():
            winner_text = f"{self.board.winner()} wins!"
            text = self.font.render(winner_text, True, BLACK)
            self.win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        if self.ai_thinking:
            text = self.font.render("AI is thinking...", True, BLACK)
            self.win.blit(text, (WIDTH // 2 - text.get_width() // 2, 10))

        pygame.display.update()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                return self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece and piece.color == self.turn:
            self.selected = (row, col)
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(*self.selected)
        if piece and (row, col) in self.valid_moves:
            self.board.move(piece, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
            return True
        return False

    def draw_valid_moves(self):
        for move in self.valid_moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        self.selected = None
        self.turn = BLACK_P if self.turn == RED_P else RED_P

    def ai_move(self):
        if self.turn == BLACK_P and not self.board.winner():
            self.ai_thinking = True
            _, new_board = minimax(self.board, 3, True)
            self.board = new_board
            self.ai_thinking = False
            self.change_turn()
