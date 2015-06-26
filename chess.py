from piece import Piece
from utils import *
import make_board
import threading

class MoveException(ChessException):
	pass

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

	def validate(self, game):
		try:
			for i in [self.x1, self.y1, self.x2, self.y2]:
				assert i >= 0 and i < 8, "invalid coordinate (%s)" % i
			assert game.turn == self.player, "It's not your turn."
			assert self.player in [BLACK, WHITE], "invalid player"
			src = game.board[self.x1][self.y1]
			dst = game.board[self.x2][self.y2]
			assert dst is None or dst.color != self.player, "can't move a piece onto another of your pieces"
			assert src is not None, "no piece at that square"
			assert src.color == self.player, "you can't move the opponent's pieces"
			self.piece = game.board[self.x1][self.y1].clone()
		except AssertionError as e:
			raise MoveException(str(e))

	def __str__(self):
		return "(%s,%s) (%s,%s) %s" % (self.y1, self.x1, self.y2, self.x2, self.piece)

class Game():
	
	def __init__(self, color, pw, game_id):
		self.game_id = game_id
		assert color in [WHITE, BLACK], "Invalid player"
		self.auth = {color: pw}
		self.moves = []
		self.board = make_board.make_board()
		self.turn = WHITE
		self.lock = threading.Lock()

	def pretty(self):
		src = self.pretty_no_borders()
		n = src.find("\n")
		header = "," + "="*26 + ".\n"
		out = header
		if self.turn == WHITE:
			color = "w"
		else:
			color = "b"
		out += ("|         " + self.game_id + " (%s)" % color).ljust(27) + "|\n"
		out += header.replace(".", "|").replace(",", "|")
		out += "|   0  1  2  3  4  5  6  7 |\n"
		out += "|%s|\n" % ("-"*26)
		for i, line in enumerate(src.split("\n")[1:-1]):
			out += "|%s| %s|\n" % (i, line)
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
		assert color not in self.auth, "player already added"
		assert color in [BLACK, WHITE], "invalid player"
		self.auth[color] = pw

	def move(self, move):
		move.validate(self)	
		self.board[move.x2][move.y2] = self.board[move.x1][move.y1]
		self.board[move.x1][move.y1] = None
		self.turn = not self.turn
		self.moves.append(move)

	@property
	def time(self):
		return len(self.moves)

	def serialize(self):
		return {"board": self.serialize_board, 
				"turn": color_to_str(self.turn),
				"moves": [str(m) for m in self.moves]
			}

	@property
	def serialize_board(self):
		out = ""
		for row in self.board:
			for piece in row:
				if piece is None:
					out += ".."
				else:
					out += str(piece)
		return out

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
