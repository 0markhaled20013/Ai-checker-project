from constants import RED_P, BLACK_P
from board import Board

def minimax(board, depth, maximizing):
    winner = board.winner()
    if depth == 0 or winner:
        return board.evaluate(), board

    color = BLACK_P if maximizing else RED_P
    best_move = None

    if maximizing:
        max_eval = float('-inf')
        for piece in board.get_all_pieces(color):
            for move, skipped in board.get_valid_moves(piece).items():
                temp = board.copy()
                temp_piece = temp.get_piece(piece.row, piece.col)
                temp.move(temp_piece, *move)
                if skipped:
                    temp.remove(skipped)
                eval, _ = minimax(temp, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = temp
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for piece in board.get_all_pieces(color):
            for move, skipped in board.get_valid_moves(piece).items():
                temp = board.copy()
                temp_piece = temp.get_piece(piece.row, piece.col)
                temp.move(temp_piece, *move)
                if skipped:
                    temp.remove(skipped)
                eval, _ = minimax(temp, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = temp
        return min_eval, best_move
