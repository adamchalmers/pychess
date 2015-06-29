from piece import Piece
from utils import *

def make_board():
	board = [[None for i in range(8)] for i in range(8)]
	board[1] = [Piece(BLACK, "P") for i in range(8)]
	board[6] = [Piece(WHITE, "P") for i in range(8)]
	board[7][0] = Piece(WHITE, "R")
	board[7][7] = Piece(WHITE, "R")
	board[0][0] = Piece(BLACK, "R")
	board[0][7] = Piece(BLACK, "R")
	board[7][1] = Piece(WHITE, "N")
	board[7][6] = Piece(WHITE, "N")
	board[0][1] = Piece(BLACK, "N")
	board[0][6] = Piece(BLACK, "N")
	board[7][2] = Piece(WHITE, "B")
	board[7][5] = Piece(WHITE, "B")
	board[0][2] = Piece(BLACK, "B")
	board[0][5] = Piece(BLACK, "B")
	board[7][3] = Piece(WHITE, "Q")
	board[7][4] = Piece(WHITE, "K")
	board[0][4] = Piece(BLACK, "Q")
	board[0][3] = Piece(BLACK, "K")

	flipped = [[None for i in range(8)] for i in range(8)]
	for i in range(8):
		for j in range(8):
			flipped[i][j] = board[j][i]
	return flipped
