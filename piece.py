from utils import WHITE, BLACK

class Piece():
	def __init__(self, color, rank):
		assert color in [BLACK, WHITE]
		assert rank in ["P", "R", "N", "B", "Q", "K"]
		self.color = color
		self.rank = rank

	def __str__(self):
		if self.color == "white":
			return "w" + self.rank
		else:
			return "b" + self.rank

	def clone(self):
		return Piece(self.color, self.rank)
