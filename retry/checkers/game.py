# import pygame
from .constants import Dark_piece, Light_piece, BLACK, ROWS, RED, COLS, WHITE
from checkers.board import Board


class Game:
    def __init__(self, boardData=[]):
        self._init(boardData)

    def _init(self, boardData=[]):
        self.selected = None
        self.board = Board(boardData)
        self.turn = Dark_piece
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)

        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            print("This move is not allowed. Please try again")
            self.selected = None
            return False

        return True

    # def draw_valid_moves(self, moves):
    #     for move in moves:
    #         row, col = move
    # pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == Dark_piece:
            self.turn = Light_piece
        else:
            self.turn = Dark_piece
        self.get_board().draw_board()

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()

    def getBoardData(self):
        result = []
        boardData = self.board.get_all_pieces(Dark_piece)
        boardData += self.board.get_all_pieces(Light_piece)
        for i in range(ROWS):
            for j in range(COLS):
                result.append(0x10);
        for piece in boardData:
            result[piece.row * COLS + piece.col] += piece.color
            if piece.king:
                result[piece.row * COLS + piece.col] += 1
        return result