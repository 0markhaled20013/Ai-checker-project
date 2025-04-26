from board import Board
from constants import RED_P, BLACK_P
from minimax import minimax
# tests
# 5 2 4 1
# 4 1 3 2
# 5 4 4 5
# 4 5 3 6
# 6 5 5 4
# 5 0 4 1
# 6 3 5 2
def main():
    board = Board()
    turn = RED_P

    while True:
        board.print_board()
        winner = board.winner()
        if winner:
            print(f"{winner} wins!")
            break

        if turn == RED_P:
            print("Your turn (Red). Enter move (from_row from_col to_row to_col):")
            try:
                fr, fc, tr, tc = map(int, input().split())
                piece = board.get_piece(fr, fc)
                if piece and piece.color == RED_P:
                    valid = board.get_valid_moves(fr, fc)
                    if (tr, tc) in valid:
                        board.move_piece(fr, fc, tr, tc)
                        turn = BLACK_P
                    else:
                        print("Invalid move. Try again.")
                else:
                    print("Invalid piece selected.")
            except:
                print("Invalid input. Try again.")
        else:
            print("AI is thinking...")
            _, new_board = minimax(board, 3, True)
            board = new_board
            turn = RED_P

if __name__ == '__main__':
    main()
