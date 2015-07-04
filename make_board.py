from piece import Piece
from utils import *

def make_board():
	board = [[None for i in range(8)] for i in range(8)]
	board[1] = [Piece.Pawn(BLACK) for i in range(8)]
	board[6] = [Piece.Pawn(WHITE) for i in range(8)]
	board[7][0] = Piece.Rook(WHITE)
	board[7][7] = Piece.Rook(WHITE)
	board[0][0] = Piece.Rook(BLACK)
	board[0][7] = Piece.Rook(BLACK)
	board[7][1] = Piece.Knight(WHITE)
	board[7][6] = Piece.Knight(WHITE)
	board[0][1] = Piece.Knight(BLACK)
	board[0][6] = Piece.Knight(BLACK)
	board[7][2] = Piece.Bishop(WHITE)
	board[7][5] = Piece.Bishop(WHITE)
	board[0][2] = Piece.Bishop(BLACK)
	board[0][5] = Piece.Bishop(BLACK)
	board[7][3] = Piece.Queen(WHITE)
	board[7][4] = Piece.King(WHITE)
	board[0][4] = Piece.Queen(BLACK)
	board[0][3] = Piece.King(BLACK)

	flipped = [[None for i in range(8)] for i in range(8)]
	for i in range(8):
		for j in range(8):
			flipped[i][j] = board[j][i]
	return flipped
