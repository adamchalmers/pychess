from utils import WHITE, BLACK

class Piece():

	def set_color(self, color):
		assert color in [BLACK, WHITE], "%s is not a color." % color
		self.color = color

	def __str__(self):
		if self.color == WHITE:
			return "w" + self.rank
		else:
			return "b" + self.rank

class King(Piece):
	def __init__(self, color):
		self.set_color(color)
		self.rank = "K"

class Queen(Piece):
	def __init__(self, color):
		self.set_color(color)
		self.rank = "Q"

class Bishop(Piece):
	def __init__(self, color):
		self.set_color(color)
		self.rank = "B"

class Knight(Piece):
	def __init__(self, color):
		self.set_color(color)
		self.rank = "N"

class Rook(Piece):
	def __init__(self, color):
		self.set_color(color)
		self.rank = "R"

class Pawn(Piece):
	def __init__(self, color):
		self.set_color(color)
		self.rank = "P"
