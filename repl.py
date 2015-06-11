from utils import *
from chess import Game, Move

def start_repl():
	game_id = raw_input("Please enter a game_id:\n")
	pw = raw_input("Please enter a password:\n")
	color = None
	while color not in ["w", "b"]:
		color = raw_input("Choose your color (w/b):\n").lower()
	if color == "w":
		color = WHITE
	else:
		color = BLACK
	g = Game(color, pw, game_id)
	print
	print g.pretty()

	move = ""
	player = color
	while move != "exit":
		try:
			movestr = raw_input("Please enter a move (x1 y1 x2 y2):\n")
		except EOFError:
			break
		try:
			x1, y1, x2, y2 = map(int, movestr.split(" "))
		except ValueError:
			print "Invalid move %s" % movestr
			continue

		try:
			move = Move(x1, y1, x2, y2, player, g)
			g.move(move)
		except AssertionError:
			print "Illegal move %s" % movestr
			continue
		print g.pretty()

if __name__ == "__main__":
	start_repl()
