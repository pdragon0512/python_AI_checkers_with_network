from copy import deepcopy

# RED = (255,0,0)
# WHITE = (255, 255, 255)
Dark_player=1
Light_player=2
def minimax(board, depth, is_max_player, game):
    if depth == 0 or board.winner() != None:
        qqq=board.evaluate()
        if board.evaluate()>0 or board.evaluate()<0:
            index=10
        return board.evaluate(), board

    if is_max_player:
        maxEval = float('-inf')
        best_move = None
        for move_board in get_all_moves(board, Dark_player, game):
            evaluation = minimax(move_board, depth-1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move_board

        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(board, Light_player, game):
            evaluation = minimax(move, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move


def get_all_moves(board, playerColor, game):
    moves = []

    for piece in board.get_all_pieces(playerColor):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            # draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)

    return moves

def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board





# def draw_moves(game, board, piece):
#     valid_moves = board.get_valid_moves(piece)
#     board.draw(game.win)
    # pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    # game.draw_valid_moves(valid_moves.keys())
    # pygame.display.update()
    #pygame.time.delay(100)

