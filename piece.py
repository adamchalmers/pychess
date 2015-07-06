from utils import WHITE, BLACK

class Piece(object):

	def __init__(self, color, x, y, char):
		assert color in [BLACK, WHITE], "%s is not a color." % color
		assert x < 8 and x >= 0, "%d is an invalid x coordinate." % x
		assert y < 8 and y >= 0, "%d is an invalid y coordinate." % y
		self.color = color
		self.x = x
		self.y = y
		self.char = char

	def __str__(self):
		if self.color == WHITE:
			return "w" + self.char
		else:
			return "b" + self.char

class King(Piece):
	def __init__(self, color, x, y):
		super(King, self).__init__(color, x, y, "K")

class Queen(Piece):
	def __init__(self, color, x, y):
		super(Queen, self).__init__(color, x, y, "Q")

class Bishop(Piece):
	def __init__(self, color, x, y):
		super(Bishop, self).__init__(color, x, y, "B")

class Knight(Piece):
	def __init__(self, color, x, y):
		super(Knight, self).__init__(color, x, y, "N")

class Rook(Piece):
	def __init__(self, color, x, y):
		super(Rook, self).__init__(color, x, y, "R")

class Pawn(Piece):
	def __init__(self, color, x, y):
		super(Pawn, self).__init__(color, x, y, "P")
