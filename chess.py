from piece import Piece
from utils import *
import make_board
class Move():
	def __init__(self, x1, y1, x2, y2, game):
		for i in [x1, y1, x2, y2]:
			assert i >= 0 and i < 8
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.piece = game[x1][y1].clone()

class Game():
	
	def __init__(self, color, auth, game_id):
		self.game_id = game_id
		assert color in [WHITE, BLACK]
		self.auth = {color: auth}
		self.moves = []
		self.board = make_board.make_board()
		self.turn = WHITE

	def pretty(self):
		out = self.game_id + "\n"
		for row in self.board:
			out += " ".join([str(piece) for piece in row]) + "\n"
		out = out.replace("None", "..")
		return out

	def check_auth(self, color, auth):
		return color in self.auth and self.auth[color] == auth

def test_small():
	g = Game(WHITE, "adampw", "adamgame")
	print g.pretty()
	assert g.check_auth(WHITE, "adampw")
	assert not g.check_auth(WHITE, "wrong pw")

if __name__ == "__main__":
	test_small()
