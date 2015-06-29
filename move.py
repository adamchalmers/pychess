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

  def validate(self, game):
    try:
      core_val(self, game)
      rank = game.board[self.x1][self.y1].rank

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
  src = game.board[m.x1][m.y1]
  dst = game.board[m.x2][m.y2]
  assert dst is None or dst.color != m.player, "You can't move a piece onto another of your pieces."
  assert src is not None, "The square you're trying to move doesn't have a piece."
  assert src.color == m.player, "You can't move the opponent's pieces."
  m.piece = game.board[m.x1][m.y1].clone()

# TODO: implement these.
def pawn_val(m, game):
  src = game.board[m.x1][m.y1]
  dst = game.board[m.x2][m.y2]
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
  pass
def king_val(m, game):
  pass
def bishop_val(m, game):
  xdist = m.x2-m.x1
  ydist = m.y2-m.y1
def rook_val(m, game, rank="Rook"):
  xdist = m.x2-m.x1
  ydist = m.y2-m.y1
  if (xdist == 0 and ydist == 0) or (xdist != 0 and ydist != 0):
    raise MoveException("%ss can only move in a straight line left, right, up or down." % rank)

  if xdist != 0:
    curr = m.x1 + xdist/abs(xdist)
    while curr < 8 and curr >= 0:
      if curr == m.x2:
        return
      if game.board[curr][m.y1] is not None:
        raise MoveException("There's a piece in your way.")
      curr += xdist/abs(xdist)
  else:
    curr = m.y1 + ydist/abs(ydist)
    while curr < 8 and curr >= 0:
      if curr == m.y2:
        return
      if game.board[m.x1][curr] is not None:
        raise MoveException("There's a piece in your way.")
      curr += ydist/abs(ydist)
  
  raise MoveException("Something very weird.")


def knight_val(m, game):
  xdist = abs(m.x1-m.x2)
  ydist = abs(m.y2-m.y1)
  if (xdist == 1 and ydist == 2) or (xdist == 2 and ydist == 1):
    return
  raise MoveException("Knights must move 2 squares in one direction and 1 square in the other direction.")


RANK_VAL = {
  "P": pawn_val,
  "Q": queen_val,
  "K": king_val,
  "B": bishop_val,
  "R": rook_val,
  "N": knight_val,
}