from piece import Piece
from utils import *
from board import Board
import threading
import move


class Game():
	
	def __init__(self, color, pw, game_id):
		self.game_id = game_id
		assert color in [WHITE, BLACK], "Invalid player"
		self.auth = {color: pw}
		self.moves = []
		self.board = Board()
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
		all_pieces = self.board.all_pieces()
		if self.turn == WHITE:
			out += " (white)\n"
		else:
			out += " (black)\n"
		for i in range(8):
			for j in range(8):
				out += str(all_pieces[j][i]) + " "
			out = out[:-1] + "\n"
		out = out.replace("None", "..")
		return out

	def check_auth(self, color, pw):
		return color in self.auth and self.auth[color] == pw

	def add_player(self, color, pw):
		assert color not in self.auth, "player already added"
		assert color in [BLACK, WHITE], "invalid player"
		self.auth[color] = pw

	def move(self, move):
		"""Executes the move encoded in a Move object on the current game."""
		move.validate(self)
		print str(move)
		self.board.move(move.x1, move.y1, move.x2, move.y2)
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
		for row in self.board.all_pieces():
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
