# import
from sys import platform
from .constants import Dark_piece, Light_piece, BLACK, ROWS, RED, COLS, WHITE,Dark_king_piece,Light_king_piece
from .piece import Piece
import os

class Board:
    def __init__(self,boardData=[]):
        self.board = []
        self.dark_left = self.light_left = 12
        self.dark_kings = self.light_kings = 0
        self.create_board(boardData)

    def create_board(self,boardData=[]):
        if boardData:
            for row in range(ROWS):
                self.board.append([])
                for col in range(COLS):
                    if boardData[row][col]==1:
                        self.board[row].append(Piece(row, col, Dark_piece))
                    if boardData[row][col] == 2:
                        self.board[row].append(Piece(row, col, Light_piece))
                    if boardData[row][col] == 3:
                        p=Piece(row, col, Dark_piece)
                        p.make_king()
                        self.board[row].append(p)
                    if boardData[row][col] == 4:
                        p = Piece(row, col, Light_piece)
                        p.make_king()
                        self.board[row].append(Piece(row, col, p))
                    if boardData[row][col] == 0:
                        self.board[row].append(0)
        else:
            for row in range(ROWS):
                self.board.append([])
                for col in range(COLS):
                    if col % 2 == ((row + 1) % 2):
                        if row < 3:
                            self.board[row].append(Piece(row, col, Dark_piece))
                        elif row > 4:
                            self.board[row].append(Piece(row, col, Light_piece))
                        else:
                            self.board[row].append(0)
                    else:
                        self.board[row].append(0)

    def draw_board(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        # if platform=="linux":
        #     os.system("clear") # in linux os.system("clear")
        # else:
        #     os.system("cls")
        print("--|--------------------- |")
        print("  | 1 2 3 4 5 6 7 8 9 10 |")
        print("--|--------------------- |")
        for i in range(ROWS):
            linetext =str(i+1)+" |";
            for j in range(COLS):
                temp=0
                if self.board[i][j]!=0:
                  temp=self.board[i][j].color
                linetext+=" "+str(temp)

            print(linetext + "  |")
        print("--|--------------------- |")


    def evaluate(self):
        return -self.light_left + self.dark_left - (self.light_kings * 0.5 - self.dark_kings * 0.5)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == Light_piece:
                self.light_kings += 1
            else:
                self.dark_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    # def draw(self, win):
    #     self.draw_squares(win)
    #     for row in range(ROWS):
    #         for col in range(COLS):
    #             piece = self.board[row][col]
    #             if piece != 0:
    #                 piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == Dark_piece:
                    self.dark_left -= 1
                else:
                    self.light_left -= 1

    def winner(self):
        if self.dark_left <= 0:
            return Light_piece  # return 2
        elif self.light_left <= 0:
            return Dark_piece  # return 1

        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == Light_piece or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == Dark_piece or piece.king:
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
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
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
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves
