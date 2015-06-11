from piece import Piece
from utils import *
import make_board

class Move():
	def __init__(self, x1, y1, x2, y2, player, game):
		self.player = player
		#print "(%d,%d) to (%d,%d)" % (x1, y1, x2, y2)
		#print game.board[y1][x1]
		#print game.board[y2][x2]
		self.x1 = y1
		self.y1 = x1
		self.x2 = y2
		self.y2 = x2
		self.validate(game)

	def validate(self, game):
		for i in [self.x1, self.y1, self.x2, self.y2]:
			assert i >= 0 and i < 8
		assert self.player in [BLACK, WHITE]
		src = game.board[self.x1][self.y1]
		dst = game.board[self.x2][self.y2]
		assert dst is None or dst.color != self.player
		assert src.color == self.player

class Game():
	
	def __init__(self, color, pw, game_id):
		self.game_id = game_id
		assert color in [WHITE, BLACK]
		self.auth = {color: pw}
		self.moves = []
		self.board = make_board.make_board()
		self.turn = WHITE

	def pretty(self):
		src = self.pretty_no_borders()
		n = src.find("\n")
		header = "," + "="*23 + ".\n"
		out = header
		out += "|      " + self.game_id + "(w)" + "     |\n"
		out += header.replace(".", "|").replace(",", "|")
		for line in src.split("\n")[1:-1]:
			out += "|" + line + "|\n"
		out += header.replace(".", "'").replace(",", "'")
		return out

	def pretty_no_borders(self):
		out = self.game_id
		if self.turn == WHITE:
			out += " (white)\n"
		else:
			out += " (black)\n"
		for row in self.board:
			out += " ".join([str(piece) for piece in row]) + "\n"
		out = out.replace("None", "..")
		return out

	def check_auth(self, color, pw):
		return color in self.auth and self.auth[color] == pw

	def add_player(self, color, pw):
		assert color not in self.auth
		assert color in [BLACK, WHITE]
		self.auth[color] = pw

	def move(self, move):
		move.validate(self)	
		self.board[move.x2][move.y2] = self.board[move.x1][move.y1]
		self.board[move.x1][move.y1] = None
		self.turn = not self.turn

def test_small():
	g = Game(WHITE, "adampw", "adamgame")
	print g.pretty()
	assert g.check_auth(WHITE, "adampw")
	assert not g.check_auth(WHITE, "wrong pw")

	g.add_player(BLACK, "black pw")
	assert g.check_auth(BLACK, "black pw")

	try:
		g.add_player(BLACK, "black 2nd pw")
	except AssertionError:
		pass

if __name__ == "__main__":
	test_small()
