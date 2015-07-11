from piece import King, Queen, Bishop, Knight, Rook, Pawn
from utils import *

class Board(object):
	"""Stores pieces on a chessboard."""
	def __init__(self):
		self._pieces = set()
		self._pieces |= {Pawn(BLACK, 1, i) for i in range(8)}
		self._pieces |= {Pawn(WHITE, 6, i) for i in range(8)}
		self._pieces.add(Rook(WHITE, 7, 0))
		self._pieces.add(Rook(WHITE, 7, 7))
		self._pieces.add(Rook(BLACK, 0, 0))
		self._pieces.add(Rook(BLACK, 0, 7))
		self._pieces.add(Knight(WHITE, 7, 1))
		self._pieces.add(Knight(WHITE, 7, 6))
		self._pieces.add(Knight(BLACK, 0, 1))
		self._pieces.add(Knight(BLACK, 0, 6))
		self._pieces.add(Bishop(WHITE, 7, 2))
		self._pieces.add(Bishop(WHITE, 7, 5))
		self._pieces.add(Bishop(BLACK, 0, 2))
		self._pieces.add(Bishop(BLACK, 0, 5))
		self._pieces.add(Queen(WHITE, 7, 3))
		self._pieces.add(King(WHITE, 7, 4))
		self._pieces.add(Queen(BLACK, 0, 4))
		self._pieces.add(King(BLACK, 0, 3))

		for piece in self._pieces:
			piece.x, piece.y = piece.y, piece.x

	def at(self, x, y):
		"""Returns the piece at the given location on the board."""
		print x, y
		for piece in self._pieces:
			if piece.x == x and piece.y == y:
				return piece
		return None

	def all_pieces(self):
		"""Returns all pieces. Faster than many calls to Board.at"""
		board = [[None for i in range(8)] for j in range(8)]
		for piece in self._pieces:
			board[piece.x][piece.y] = piece
		return board

	def move(self, piece, x, y):
		"""Moves the piece to x, y, removing any piece previously there."""
		assert piece is not None
		if self.at(x, y) is not None:
			self._pieces.remove(self.at(x,y))
		assert self.at(x,y) is None
		piece.x = x
		piece.y = y

