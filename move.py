from utils import *

class MoveException(ChessException):
  pass

class Move():
  def __init__(self, x1, y1, x2, y2, player, game):
    self.player = player
    self.x1 = x1
    self.y1 = y1
    self.x2 = x2
    self.y2 = y2
    self.piece = str(game.board.at(x1, y1))

  def validate(self, game):
    try:
      core_val(self, game)
      rank = game.board.at(self.x1, self.y1).char

      RANK_VAL[rank](self, game)

    except AssertionError as e:
      raise MoveException(str(e))

  def __str__(self):
    return "(%s,%s) (%s,%s) %s" % (self.y1, self.x1, self.y2, self.x2, self.piece)

def core_val(m, game):
  # Basic rules of chess
  for i in [m.x1, m.y1, m.x2, m.y2]:
    assert i >= 0 and i < 8, "Invalid coordinate (%s)." % i
  assert game.turn == m.player, "It's not your turn."
  assert m.player in [BLACK, WHITE], "Invalid player."
  src = game.board.at(m.x1, m.y1)
  dst = game.board.at(m.x2, m.y2)
  assert dst is None or dst.color != m.player, "You can't move a piece onto another of your pieces."
  assert src is not None, "The square you're trying to move doesn't have a piece."
  assert src.color == m.player, "You can't move the opponent's pieces."

def pawn_val(m, game):
  src = game.board.at(m.x1, m.y1)
  dst = game.board.at(m.x2, m.y2)
  xdist = abs(m.x1-m.x2)
  ydist = m.y2-m.y1

  # Check the player hasn't moved backwards
  if (m.player == BLACK and ydist <= 0) or (m.player == WHITE and ydist >= 0):
    raise MoveException("You can't move pawns backwards.")

  # Moving directly forward (no capture)
  if xdist == 0 and dst == None:

    # You can move forward 2 squares from your starting row
    if abs(ydist) == 2:
      if (m.player == BLACK and m.y1 == 1) or (m.player == WHITE and m.y1 == 6):
        return
    # Otherwise you can move forward one square
    elif abs(ydist) == 1:
      return

  # Capturing diagonally:
  if xdist == 1 and abs(ydist) == 1 and dst is not None:
    if src.color != dst.color:
      return

  # TODO: add en passant.
  # This and castling will require tagging the game state when moves are processed,
  # so you can look at tags like 'check' or 'en passant' or 'castleable' to see if an action is valid.

  raise MoveException("Pawns can either move 1 square forward, 2 squares forward from their starting position, or diagonally-forward one square to capture.")


def queen_val(m, game):

  # Return if it's a legal rook move, otherwise keep trying.
  try:
    rook_val(m, game)
    return
  except MoveException:
    pass

  # Return if it's a legal bishop move, otherwise error.
  try:
    bishop_val(m, game)
    return
  except MoveException:
    raise MoveException("Your queen can't move there. Queens can move like bishops or like rooks.")

def king_val(m, game):
  xdist = m.x2-m.x1
  ydist = m.y2-m.y1

  # TODO: Add castling.

  if abs(xdist) > 1 or abs(ydist) > 1:
    raise MoveException("Kings can only move one square away.")

  # Kings can't move next to other kings
  for i in range(m.x2-1, m.x2+2):
    for j in range(m.y2-1, m.y2+2):
      target = game.board.at(i,j)
      if target is not None and target.rank == "K":
        raise MoveException("A king can't move next to another king.")

def bishop_val(m, game):
  xdist = m.x2-m.x1
  ydist = m.y2-m.y1

  if (abs(xdist) != abs(ydist)):
    raise MoveException("Bishops must move diagonally.")

  path_clear(m, game, xdist/abs(xdist), ydist/abs(ydist))



def rook_val(m, game):
  xdist = m.x2-m.x1
  ydist = m.y2-m.y1
  if (xdist == 0 and ydist == 0) or (xdist != 0 and ydist != 0):
    raise MoveException("Rooks can only move in a straight line left, right, up or down.")

  if xdist != 0:
    path_clear(m, game, xdist/abs(xdist), 0)
    return
  else:
    path_clear(m, game, 0, ydist/abs(ydist))
    return

  raise MoveException("Something very weird.")


def knight_val(m, game):
  xdist = abs(m.x1-m.x2)
  ydist = abs(m.y2-m.y1)
  if (xdist == 1 and ydist == 2) or (xdist == 2 and ydist == 1):
    return
  raise MoveException("Knights must move 2 squares in one direction and 1 square in the other direction.")

def path_clear(m, game, dx, dy):
  """Checks if the path from m's start to m's end is clear."""
  x = m.x1 + dx
  y = m.y1 + dy
  while x < 8 and y < 8 and x >= 0 and y >= 0:
    if m.x2 == x and m.y2 == y:
      return
    if game.board.at(x,y) is not None:
      raise MoveException("There's a piece in your way.")
    x += dx
    y += dy
  raise MoveException("You can't reach that point.")

RANK_VAL = {
  "P": pawn_val,
  "Q": queen_val,
  "K": king_val,
  "B": bishop_val,
  "R": rook_val,
  "N": knight_val,
}
