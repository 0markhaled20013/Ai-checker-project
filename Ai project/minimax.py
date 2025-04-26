from constants import RED_P, BLACK_P

def minimax(board, depth, maximizing):
    winner = board.winner()
    if depth == 0 or winner:
        return board.evaluate(), board

    color = BLACK_P if maximizing else RED_P
    best_move = None
    if maximizing:
        max_eval = float('-inf')
        for move in board.get_all_moves(color):
            temp_board = board.copy()
            temp_board.move_piece(*move[0], *move[1])
            eval, _ = minimax(temp_board, depth - 1, False)
            if eval > max_eval:
                max_eval = eval
                best_move = temp_board
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in board.get_all_moves(color):
            temp_board = board.copy()
            temp_board.move_piece(*move[0], *move[1])
            eval, _ = minimax(temp_board, depth - 1, True)
            if eval < min_eval:
                min_eval = eval
                best_move = temp_board
        return min_eval, best_move
