from piece import King, Queen, Bishop, Knight, Rook, Pawn
from utils import *

def make_board():
	board = [[None for i in range(8)] for i in range(8)]
	board[1] = [Pawn(BLACK) for i in range(8)]
	board[6] = [Pawn(WHITE) for i in range(8)]
	board[7][0] = Rook(WHITE)
	board[7][7] = Rook(WHITE)
	board[0][0] = Rook(BLACK)
	board[0][7] = Rook(BLACK)
	board[7][1] = Knight(WHITE)
	board[7][6] = Knight(WHITE)
	board[0][1] = Knight(BLACK)
	board[0][6] = Knight(BLACK)
	board[7][2] = Bishop(WHITE)
	board[7][5] = Bishop(WHITE)
	board[0][2] = Bishop(BLACK)
	board[0][5] = Bishop(BLACK)
	board[7][3] = Queen(WHITE)
	board[7][4] = King(WHITE)
	board[0][4] = Queen(BLACK)
	board[0][3] = King(BLACK)

	flipped = [[None for i in range(8)] for i in range(8)]
	for i in range(8):
		for j in range(8):
			flipped[i][j] = board[j][i]
	return flipped
