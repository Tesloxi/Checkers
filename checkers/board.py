from pygame import Surface, draw 
from .constants import *
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.black_left = self.beige_left = 12
        self.black_kings = self.beige_kings = 0
        self.create_board()

    def draw_squares(self, surface):
        surface.fill(BROWN)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                draw.rect(surface, BEIGE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == BEIGE:
                self.beige_kings += 1
            else:
                self.black_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, BEIGE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, surface):
        self.draw_squares(surface)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(surface)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.black_left -= 1
                else:
                    self.beige_left -= 1

    def winner(self):
        if self.black_left <= 0:
            return BEIGE
        elif self.beige_left <= 0:
            return BLACK
        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BLACK or piece.king:
            moves.update(self._traverse_left(row - 1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row-3, -1), -1, piece.color, right))

        if piece.color == BEIGE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row+3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped=last))
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
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped=last))
                break
                    
            elif current.color == color:
                break
            else:
                last = [current]
            right += 1

        return moves