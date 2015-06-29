from utils import *

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
  pass
def queen_val(m, game):
  pass
def king_val(m, game):
  pass
def bishop_val(m, game):
  pass
def rook_val(m, game):
  pass
def knight_val(m, game):
  pass


RANK_VAL = {
  "P": pawn_val,
  "Q": queen_val,
  "K": king_val,
  "B": bishop_val,
  "R": rook_val,
  "N": knight_val,
}