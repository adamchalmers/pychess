from utils import WHITE, BLACK

class Piece():

	def __init__(self, rank, color):
		assert color in [BLACK, WHITE], "%s is not a color." % color
		self.rank = rank
		self.color = color

	@staticmethod
	def King(color):
		return Piece("K", color)

	@staticmethod
	def Queen(color):
		return Piece("Q", color)

	@staticmethod
	def Bishop(color):
		return Piece("B", color)

	@staticmethod
	def Knight(color):
		return Piece("N", color)

	@staticmethod
	def Rook(color):
		return Piece("R", color)

	@staticmethod
	def Pawn(color):
		return Piece("P", color)

	def __str__(self):
		if self.color == WHITE:
			return "w" + self.rank
		else:
			return "b" + self.rank
