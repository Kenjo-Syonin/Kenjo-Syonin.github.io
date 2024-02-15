import pygame
import time
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 800
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animation
IMAGES = {}

# Initialize a dictionary of images
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK',
              'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = pygame.image.load('images/' + piece + '.png')

# Returns a list of all valid moves for a piece
def getAllPossibleMoves(piece, board):
    moves = []
    if piece.type == 'p':
        if piece.team == 'w':
            moves = getPawnMoves(piece.position, board, True)
        else:
            moves = getPawnMoves(piece.position, board, False)
    elif piece.type == 'R':
        moves = getRookMoves(piece.position, board)
    elif piece.type == 'N':
        moves = getKnightMoves(piece.position, board)
    elif piece.type == 'B':
        moves = getBishopMoves(piece.position, board)
    elif piece.type == 'Q':
        moves = getQueenMoves(piece.position, board)
    elif piece.type == 'K':
        moves = getKingMoves(piece.position, board)
    return moves

# Determine all possible squares a pawn can move to
def getPawnMoves(position, board, isWhite):
    moves = []
    row, col = position
    if isWhite:
        if board[row-1][col] == '--':  # empty space
            moves.append((row-1, col))
        if col-1 >= 0:
            if board[row-1][col-1][0] == 'b':  # capture
                moves.append((row-1, col-1))
        if col+1 < DIMENSION:
            if board[row-1][col+1][0] == 'b':  # capture
                moves.append((row-1, col+1))
        # en passant
        if col-1 >= 0 and board[row-1][col-1] == 'bp':
            if row-2 >= 0 and board[row-2][col-1] == '--':
                moves.append((row-2, col-1))
        if col+1 < DIMENSION and board[row-1][col+1] == 'bp':
            if row-2 >= 0 and board[row-2][col+1] == '--':
                moves.append((row-2, col+1))
        # two-step move
        if row-2 >= 0 and board[row-2][col] == '--':
            if board[row-1][col] == '--' and board[row-2][col][0] != 'b':
                moves.append((row-2, col))
    else:
        if board[row+1][col] == '--':  # empty space
            moves.append((row+1, col))
        if col-1 >= 0:
            if board[row+1][col-1][0] == 'w':  # capture
                moves.append((row+1, col-1))
        if col+1 < DIMENSION:
            if board[row+1][col+1][0] == 'w':  # capture
                moves.append((row+1, col+1))
        # en passant
        if col-1 >= 0 and board[row+1][col-1] == 'wp':
            if row+2 < DIMENSION and board[row+2][col-1] == '--':
                moves.append((row+2, col-1))
        if col+1 < DIMENSION and board[row+1][col+1] == 'wp':
            if row+2 < DIMENSION and board[row+2][col+1] == '--':
                moves.append((row+2, col+1))
        # two-step move
        if row+2 < DIMENSION and board[row+2][col] == '--':
            if board[row+1][col] == '--' and board[row+2][col][0] != 'w':
                moves.append((row+2, col))
    return moves

# Determine all possible squares a rook can move to
def getRookMoves(position, board):
    moves = []
    row, col = position
    # up
    for i in range(row-1, -1, -1):
        if board[i][col] == '--':
            moves.append((i, col))
        elif board[i][col][0] != board[row][col][0]:
            moves.append((i, col))
            break
    # down
    for i in range(row+1, DIMENSION):
        if board[i][col] == '--':
            moves.append((i, col))
        elif board[i][col][0] != board[row][col][0]:
            moves.append((i, col))
            break
    # left
    for i in range(col-1, -1, -1):
        if board[row][i] == '--':
            moves.append((row, i))
        elif board[row][i][0] != board[row][col][0]:
            moves.append((row, i))
            break
    # right
    for i in range(col+1, DIMENSION):
        if board[row][i] == '--':
            moves.append((row, i))
        elif board[row][i][0] != board[row][col][0]:
            moves.append((row, i))
            break
    return moves

# Determine all possible squares a knight can move to
def getKnightMoves(