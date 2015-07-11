from utils import *

def validate(move, game):
  try:

    # Run general move validation.
    core_val(move, game)

    # Use a select/case to validate based on piece-specific rules.
    rank = game.board.at(move.piece.x, move.piece.y).char
    {"P": pawn_val,
     "Q": queen_val,
     "K": king_val,
     "B": bishop_val,
     "R": rook_val,
     "N": knight_val,
    }[rank](move, game)

  except AssertionError as e:
    raise MoveException(str(e))

def core_val(m, game):
  # Basic rules of chess
  for i in [m.piece.x, m.piece.y, m.x, m.y]:
    assert i >= 0 and i < 8, "Invalid coordinate (%s)." % i
  assert game.turn == m.player, "It's not your turn."
  assert m.player in [BLACK, WHITE], "Invalid player."
  dst = game.board.at(m.x, m.y)
  assert dst is None or dst.color != m.player, "You can't move a piece onto another of your pieces."
  assert m.piece is not None, "The square you're trying to move doesn't have a piece."
  assert m.piece.color == m.player, "You can't move the opponent's pieces."

def pawn_val(m, game):
  dst = game.board.at(m.x, m.y)
  xdist = abs(m.piece.x-m.x)
  ydist = m.y-m.piece.y

  # Check the player hasn't moved backwards
  if (m.player == BLACK and ydist <= 0) or (m.player == WHITE and ydist >= 0):
    raise MoveException("You can't move pawns backwards.")

  # Moving directly forward (no capture)
  if xdist == 0 and dst == None:

    # You can move forward 2 squares from your starting row
    if abs(ydist) == 2:
      if (m.player == BLACK and m.piece.y == 1) or (m.player == WHITE and m.piece.y == 6):
        return
    # Otherwise you can move forward one square
    elif abs(ydist) == 1:
      return

  # Capturing diagonally:
  if xdist == 1 and abs(ydist) == 1 and dst is not None:
    if m.piece.color != dst.color:
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
  xdist = m.x-m.piece.x
  ydist = m.y-m.piece.y

  # TODO: Add castling.

  if abs(xdist) > 1 or abs(ydist) > 1:
    raise MoveException("Kings can only move one square away.")

  # Kings can't move next to other kings
  for i in range(m.x-1, m.x+2):
    for j in range(m.y-1, m.y+2):
      target = game.board.at(i,j)
      if target is not None and target.rank == "K":
        raise MoveException("A king can't move next to another king.")

def bishop_val(m, game):
  xdist = m.x-m.piece.x
  ydist = m.y-m.piece.y

  if (abs(xdist) != abs(ydist)):
    raise MoveException("Bishops must move diagonally.")

  path_clear(m, game, xdist/abs(xdist), ydist/abs(ydist))



def rook_val(m, game):
  xdist = m.x-m.piece.x
  ydist = m.y-m.piece.y
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
  xdist = abs(m.piece.x-m.x)
  ydist = abs(m.y-m.piece.y)
  if (xdist == 1 and ydist == 2) or (xdist == 2 and ydist == 1):
    return
  raise MoveException("Knights must move 2 squares in one direction and 1 square in the other direction.")

def path_clear(m, game, dx, dy):
  """Checks if the path from m's start to m's end is clear."""
  x = m.piece.x + dx
  y = m.piece.y + dy
  while x < 8 and y < 8 and x >= 0 and y >= 0:
    if m.x == x and m.y == y:
      return
    if game.board.at(x,y) is not None:
      raise MoveException("There's a piece in your way.")
    x += dx
    y += dy
  raise MoveException("You can't reach that point.")