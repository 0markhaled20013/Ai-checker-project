import pygame
import copy
from constants import *
from piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.black_left = 12
        self.red_kings = self.black_kings = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(WHITE)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, GREY, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(BLACK_P, row, col))
                    elif row > 4:
                        self.board[row].append(Piece(RED_P, row, col))
                    else:
                        self.board[row].append(None)
                else:
                    self.board[row].append(None)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece:
                    piece.draw(win)

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = None, piece
        piece.move(row, col)
        if row == 0 and piece.color == RED_P:
            piece.make_king()
            self.red_kings += 1
        elif row == ROWS - 1 and piece.color == BLACK_P:
            piece.make_king()
            self.black_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = None
            if piece.color == RED_P:
                self.red_left -= 1
            else:
                self.black_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return "Black"
        elif self.black_left <= 0:
            return "Red"
        return None

    def evaluate(self):
        return self.black_left - self.red_left + (self.black_kings * 0.5 - self.red_kings * 0.5)

    def get_all_pieces(self, color):
        return [piece for row in self.board for piece in row if piece and piece.color == color]

    def copy(self):
        new_board = Board()
        new_board.board = copy.deepcopy(self.board)
        new_board.red_left = self.red_left
        new_board.black_left = self.black_left
        new_board.red_kings = self.red_kings
        new_board.black_kings = self.black_kings
        return new_board

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED_P or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == BLACK_P or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            if current is None:
                if skipped and not last:
                    break
                moves[(r, left)] = last + skipped if skipped else last
                if last:
                    row_limit = max(r - 3, -1) if step == -1 else min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row_limit, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row_limit, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            left -= 1
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current is None:
                if skipped and not last:
                    break
                moves[(r, right)] = last + skipped if skipped else last
                if last:
                    row_limit = max(r - 3, -1) if step == -1 else min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row_limit, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row_limit, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            right += 1
        return moves
