from constants import RED_P, BLACK_P

class Piece:
    def __init__(self, color, king=False):
        self.color = color
        self.king = king

    def make_king(self):
        self.king = True

    def __repr__(self):
        if self.color == RED_P:
            return 'R' if not self.king else 'RK'
        elif self.color == BLACK_P:
            return 'B' if not self.king else 'BK'
        return '.'
