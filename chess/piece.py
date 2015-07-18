from utils import WHITE, BLACK, path_clear, MoveException
import outcomes

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
    Throws an exception if the move would be invalid.
    If the move is valid, it None or a string describing a special move outcome."""
    raise NotImplementedError()

  def can_attack(self, board, x, y):
    """Default behaviour just calls can_move. Should be overridden for pawns."""
    return self.can_move(board, x, y)

  def after_move(self):
    """Called after the piece has moved. Default implementation is no-op.
    Override for pieces which care about having moved, like king/pawn."""
    return

  def copy(self):
    t = type(self)
    return t(self.color, self.x, self.y)

  def __str__(self):
    if self.color == WHITE:
      return "w" + self.char
    else:
      return "b" + self.char


class King(Piece):

  def __init__(self, color, x, y):
    super(King, self).__init__(color, x, y, "K")
    self.has_moved = False # If true, can't castle.

  def after_move(self):
    self.has_moved = True

  def can_move(self, board, x, y):
    xdist = x-self.x
    ydist = y-self.y

    # outcomes.CASTLING rules
    outcomes.CASTLING = False
    if self.has_moved == False and ydist == 0:
      if xdist == -2 and self.color == WHITE and board.at(0,7) is not None and board.at(0,7).char == "R":
        return outcomes.CASTLING, 0, 7, 2, 7
      if xdist == -2 and self.color == BLACK and board.at(0,0) is not None and board.at(0,0).char == "R":
        return outcomes.CASTLING, 0, 0, 2, 0
      if xdist == 3 and self.color == WHITE and board.at(7,7) is not None and board.at(7,7).char == "R":
        return outcomes.CASTLING, 7, 7, 5, 7
      if xdist == 3 and self.color == BLACK and board.at(7,0) is not None and board.at(7,0).char == "R":
        return outcomes.CASTLING, 7, 0, 5, 0

    if abs(xdist) > 1 or abs(ydist) > 1:
      raise MoveException("Kings can only move one square away.")

    # Kings can't move next to other kings
    for i in range(x-1, x+2):
      for j in range(y-1, y+2):
        target = board.at(i,j)
        if target is not None and target is not self and target.char == "K":
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

    path_clear(self, board, x, y)


class Knight(Piece):

  def __init__(self, color, x, y):
    super(Knight, self).__init__(color, x, y, "N")

  def can_move(self, board, x, y):
    xdist = abs(x-self.x)
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

    path_clear(self, board, x, y)


class Pawn(Piece):
  def __init__(self, color, x, y):
    super(Pawn, self).__init__(color, x, y, "P")
    self.en_passantable = False
    self.jumped = False

  def after_move(self):
    if self.jumped:
      self.jumped = False
      self.en_passantable = True
    else:
      self.en_passantable = False

  def can_move(self, board, x, y):

    dst = board.at(x, y)
    xdist = x-self.x
    ydist = y-self.y

    # Check the player hasn't moved backwards
    if (self.color == BLACK and ydist <= 0) or (self.color == WHITE and ydist >= 0):
      raise MoveException("You can't move pawns backwards.")

    # Moving directly forward (no capture)
    if abs(xdist) == 0 and dst == None:

      # You can move forward 2 squares from your starting row
      if abs(ydist) == 2:
        if (self.color == BLACK and self.y == 1) or (self.color == WHITE and self.y == 6):
          self.jumped = True
          return
      # Otherwise you can move forward one square
      elif abs(ydist) == 1:
        if (self.color == WHITE and y == 0) or (self.color == BLACK and y == 7):
          return outcomes.PROMOTING, 
        return

    # Check en passant
    if abs(xdist) == 1:
      target = board.at(self.x+xdist, self.y)
      if (ydist == 1 and self.color == BLACK and type(target) == Pawn and target.en_passantable) or (
        ydist == -1 and self.color == WHITE and type(target) == Pawn and target.en_passantable):
        return outcomes.EN_PASSANTING, self.x+xdist, self.y
    raise MoveException("Pawns can only move 1 square forward (or 2 from their starting position).")

  def can_attack(self, board, x, y):
    # TODO: add en passant.
    # This and outcomes.CASTLING will require tagging the board state when moves are processed,
    # so you can look at tags like 'check' or 'en passant' or 'castleable' to see if an action is valid.
    xdist = x-self.x
    ydist = y-self.y
    if (self.color == BLACK and ydist <= 0) or (self.color == WHITE and ydist >= 0):
      raise MoveException("You can't move pawns backwards.")
    if abs(xdist) != 1 or abs(ydist) != 1:
      raise MoveException("Pawns can only capture pieces diagonally in front of them.")

