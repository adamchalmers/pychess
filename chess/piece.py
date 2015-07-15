from utils import WHITE, BLACK, path_clear, MoveException

class Piece(object):

	def __init__(self, color, x, y, char):
		assert color in [BLACK, WHITE], "%s is not a color." % color
		assert x < 8 and x >= 0, "%d is an invalid x coordinate." % x
		assert y < 8 and y >= 0, "%d is an invalid y coordinate." % y
		self.color = color
		self.x = x
		self.y = y
		self.char = char

	def can_move(self, board, x, y):
		"""Used to validate moves.
		Throws an exception if the move would be invalid. Returns None otherwise."""
		raise NotImplementedError()

	def can_attack(self, board, x, y):
		"""Default behaviour just calls can_move. Should be overridden for pawns."""
		return self.can_move(board, x, y)

	def __str__(self):
		if self.color == WHITE:
			return "w" + self.char
		else:
			return "b" + self.char


class King(Piece):

	def __init__(self, color, x, y):
		super(King, self).__init__(color, x, y, "K")

	def can_move(self, board, x, y):
	  xdist = x-self.x
	  ydist = y-self.y

	  # TODO: Add castling.

	  if abs(xdist) > 1 or abs(ydist) > 1:
	    raise MoveException("Kings can only move one square away.")

	  # Kings can't move next to other kings
	  for i in range(x-1, x+2):
	    for j in range(y-1, y+2):
	      target = board.at(i,j)
	      if target is not None and target.rank == "K":
	        raise MoveException("A king can't move next to another king.")


class Queen(Piece):

	def __init__(self, color, x, y):
		super(Queen, self).__init__(color, x, y, "Q")

	def can_move(self, board, x, y):

	  # Return if it's a legal rook move, otherwise keep trying.
	  try:
	    Bishop(self.color, self.x, self.y).can_move(board, x, y)
	    return
	  except MoveException:
	    pass

	  # Return if it's a legal bishop move, otherwise error.
	  try:
	    Rook(self.color, self.x, self.y).can_move(board, x, y)
	    return
	  except MoveException:
	    raise MoveException("Your queen can't move there. Queens can move like bishops or like rooks.")


class Bishop(Piece):

	def __init__(self, color, x, y):
		super(Bishop, self).__init__(color, x, y, "B")

	def can_move(self, board, x, y):
	  xdist = x-self.x
	  ydist = y-self.y

	  if (abs(xdist) != abs(ydist)):
	    raise MoveException("Bishops must move diagonally.")

	  path_clear(self, board, xdist/abs(xdist), ydist/abs(ydist), x, y)


class Knight(Piece):

	def __init__(self, color, x, y):
		super(Knight, self).__init__(color, x, y, "N")

	def can_move(self, board, x, y):
	  xdist = abs(self.x-x)
	  ydist = abs(y-self.y)
	  if (xdist == 1 and ydist == 2) or (xdist == 2 and ydist == 1):
	    return
	  raise MoveException("Knights must move 2 squares in one direction and 1 square in the other direction.")


class Rook(Piece):

	def __init__(self, color, x, y):
		super(Rook, self).__init__(color, x, y, "R")

	def can_move(self, board, x, y):
	  xdist = x-self.x
	  ydist = y-self.y
	  if (xdist == 0 and ydist == 0) or (xdist != 0 and ydist != 0):
	    raise MoveException("Rooks can only move in a straight line left, right, up or down.")

	  if xdist != 0:
	    path_clear(self, board, xdist/abs(xdist), 0, x, y)
	    return
	  else:
	    path_clear(self, board, 0, ydist/abs(ydist), x, y)
	    return

	  raise MoveException("Something very weird.")


class Pawn(Piece):
	def __init__(self, color, x, y):
		super(Pawn, self).__init__(color, x, y, "P")

	def can_move(self, board, x, y):

	  dst = board.at(x, y)
	  xdist = abs(self.x-x)
	  ydist = y-self.y

	  # Check the player hasn't moved backwards
	  if (self.color == BLACK and ydist <= 0) or (self.color == WHITE and ydist >= 0):
	    raise MoveException("You can't move pawns backwards.")

	  # Moving directly forward (no capture)
	  if xdist == 0 and dst == None:

	    # You can move forward 2 squares from your starting row
	    if abs(ydist) == 2:
	      if (self.color == BLACK and self.y == 1) or (self.color == WHITE and self.y == 6):
	        return
	    # Otherwise you can move forward one square
	    elif abs(ydist) == 1:
	      return

	  raise MoveException("Pawns can only move 1 square forward (or 2 from their starting position).")

	def can_attack(self, board, x, y):
	  # TODO: add en passant.
	  # This and castling will require tagging the board state when moves are processed,
	  # so you can look at tags like 'check' or 'en passant' or 'castleable' to see if an action is valid.
	  xdist = abs(self.x-x)
	  ydist = y-self.y
	  if xdist != 1 or abs(ydist) != 1:
			raise MoveException("Pawns can only capture pieces diagonally in front of them.")
