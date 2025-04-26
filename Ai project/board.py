import copy
from piece import Piece
from constants import  RED_P, BLACK_P

class Board:
# the full 8x8 board
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = Piece(BLACK_P)
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = Piece(RED_P)
        return board

    def print_board(self):
        print("  0 1 2 3 4 5 6 7")
        for i, row in enumerate(self.board):
            print(i, end=" ")
            for piece in row:
                if piece:
                    print(piece, end=" ")
                else:
                    print('.', end=" ")
            print()

    def get_piece(self, row, col):
        return self.board[row][col]

    def move_piece(self, from_row, from_col, to_row, to_col):
        piece = self.board[from_row][from_col]
        self.board[from_row][from_col] = None
        self.board[to_row][to_col] = piece
        if to_row == 0 and piece.color == RED_P:
            piece.make_king()
        if to_row == 7 and piece.color == BLACK_P:
            piece.make_king()

        if abs(from_row - to_row) == 2:
            jumped_row = (from_row + to_row) // 2
            jumped_col = (from_col + to_col) // 2
            self.board[jumped_row][jumped_col] = None

    def get_all_pieces(self, color):
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    pieces.append((row, col))
        return pieces

    def get_valid_moves(self, row, col):
        piece = self.board[row][col]
        if not piece:
            return {}
        moves = {}
        directions = [(-1, -1), (-1, 1)] if piece.color == RED_P else [(1, -1), (1, 1)]
        if piece.king:
            directions += [(-d[0], -d[1]) for d in directions]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] is None:
                moves[(r, c)] = []
            elif 0 <= r < 8 and 0 <= c < 8:
                enemy = self.board[r][c]
                if enemy and enemy.color != piece.color:
                    r2, c2 = r + dr, c + dc
                    if 0 <= r2 < 8 and 0 <= c2 < 8 and self.board[r2][c2] is None:
                        moves[(r2, c2)] = [(r, c)]
        return moves

    def evaluate(self):
        red_score = 0
        black_score = 0
        for row in self.board:
            for piece in row:
                if piece:
                    if piece.color == RED_P:
                        red_score += 1 + (0.5 if piece.king else 0)
                    elif piece.color == BLACK_P:
                        black_score += 1 + (0.5 if piece.king else 0)
        return black_score - red_score

    def get_all_moves(self, color):
        moves = []
        for (r, c) in self.get_all_pieces(color):
            valid = self.get_valid_moves(r, c)
            for move, captures in valid.items():
                moves.append(((r, c), move, captures))
        return moves

    def copy(self):
        new_board = Board()
        new_board.board = copy.deepcopy(self.board)
        return new_board

    def winner(self):
        red = black = 0
        for row in self.board:
            for piece in row:
                if piece:
                    if piece.color == RED_P:
                        red += 1
                    elif piece.color == BLACK_P:
                        black += 1
        if red == 0:
            return 'Black'
        elif black == 0:
            return 'Red'
        return None
