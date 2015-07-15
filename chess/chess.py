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
		self.board = Board()
		self.turn = WHITE
		self.lock = threading.Lock()
		self.turns = 0

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
		move.validate()
		print str(move)
		self.board.move(move.piece, move.x, move.y)
		self.turn = not self.turn
		self.turns += 1

	def serialize(self):
		return {"board": self.serialize_board, 
				"turn": color_to_str(self.turn),
				"time": self.turns
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

def test_auth():
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

def test_game_small():
	g = Game(WHITE, "pw", "game1")
	g.add_player(BLACK, "pw")
	m1 = move.Move(0, 6, 0, 4, WHITE, g)
	g.move(m1)
	m2 = move.Move(1, 1, 1, 3, BLACK, g)
	g.move(m2)
	m3 = move.Move(5, 6, 5, 5, WHITE, g)
	g.move(m3)
	m4 = move.Move(1, 3, 0, 4, BLACK, g)
	g.move(m4)
	m5 = move.Move(0, 7, 0, 4, WHITE, g)
	g.move(m5)

if __name__ == "__main__":
	test_small()
