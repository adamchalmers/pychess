from piece import King, Queen, Bishop, Knight, Rook, Pawn
from utils import *

def make_board():
	board = [[None for i in range(8)] for i in range(8)]
	board[1] = [Pawn(BLACK, 1, i) for i in range(8)]
	board[6] = [Pawn(WHITE, 6, i) for i in range(8)]
	board[7][0] = Rook(WHITE, 7, 0)
	board[7][7] = Rook(WHITE, 7, 7)
	board[0][0] = Rook(BLACK, 0, 0)
	board[0][7] = Rook(BLACK, 0, 0)
	board[7][1] = Knight(WHITE, 7, 1)
	board[7][6] = Knight(WHITE, 7, 6)
	board[0][1] = Knight(BLACK, 0, 1)
	board[0][6] = Knight(BLACK, 0, 6)
	board[7][2] = Bishop(WHITE, 7, 2)
	board[7][5] = Bishop(WHITE, 7, 5)
	board[0][2] = Bishop(BLACK, 0, 2)
	board[0][5] = Bishop(BLACK, 0, 5)
	board[7][3] = Queen(WHITE, 7, 3)
	board[7][4] = King(WHITE, 7, 4)
	board[0][4] = Queen(BLACK, 0, 4)
	board[0][3] = King(BLACK, 0, 3)

	flipped = [[None for i in range(8)] for i in range(8)]
	for i in range(8):
		for j in range(8):
			trans = board[j][i]
			flipped[i][j] = trans
			if trans is not None:
				flipped[i][j].x, flipped[i][j].y = trans.y, trans.x
	return flipped
